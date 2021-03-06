#cython: language_level=3

import os
import glob
import shutil
import requests
import setuptools

from colorama import Fore, init
from distutils.core import setup
from Cython.Distutils import build_ext
from distutils.extension import Extension

init(autoreset=True)
HIDDEN_IMPORTS = "['main', 'colorama', 'requests', 'pynput', 'pyinstaller', 'discord', 'threading', 'time'],\n"
PROGRAM_NAME = "word"


def cythonize():
    ext_modules = [
        Extension('main', ['main.py']),
    ]
    setup(
        name=PROGRAM_NAME,
        cmdclass={'build_ext': build_ext},
        script_args=['build_ext', '--inplace'],
        ext_modules=ext_modules
    )


def clearCompiledFolder():
    files = glob.glob('compiled/*')
    for i in files:
        if 'dummy.py' in i:
            continue

        if os.path.isdir(i):
            shutil.rmtree(i)
        else:
            os.remove(i)


def moveCompiledCodeToFolder():
    # Move compiled files into a folder
    files = glob.glob('./*.so')
    files.extend(glob.glob('./*.pyd'))
    for i in files:
        shutil.move(i, './compiled')


def deleteOldFiles():
    files = glob.glob('./*.so')
    files.extend(glob.glob('./*.pyd'))
    files.extend(glob.glob('./*.c'))

    for i in files:
        os.remove(i)


def generateSpecFile():
    os.system(f'pyi-makespec dummy.py -n {PROGRAM_NAME} --onefile')

    with open(f'{PROGRAM_NAME}.spec', 'r') as f:
        lines = f.readlines()

    for i, x in enumerate(lines):
        if 'hiddenimports' in x:
            lines[i] = '\t\t\thiddenimports=' + HIDDEN_IMPORTS
        if 'console=' in x:
            lines[i] = '\t\t\tconsole=True,\n)'

    with open(f'{PROGRAM_NAME}.spec', 'w') as f:
        f.writelines(lines)

    shutil.move(f'./{PROGRAM_NAME}.spec', './compiled')


def createExe():
    os.system(
        f'cd ./compiled && pyinstaller {PROGRAM_NAME}.spec --clean --onefile')
    name = PROGRAM_NAME if os.name != 'nt' else PROGRAM_NAME + '.exe'

    # If the .exe already exists, then delete it
    if os.path.isfile(name):
        os.remove(name)

    shutil.move(os.path.join('compiled', 'dist', name), './')


def compileProgram():
    clearCompiledFolder()

    cythonize()
    moveCompiledCodeToFolder()
    generateSpecFile()
    createExe()

if __name__ == '__main__':
    # Make sure this directory exists first
    if not os.path.isdir('./compiled'):
        os.makedirs('./compiled')

    # Create dummy file that will run the compiled C code
    with open('./compiled/dummy.py', 'w') as f:
        f.write("from main import main\nif __name__ == '__main__':\n\tmain()")

    # Check for any other builds
    fileNames = glob.glob('./*.exe')
    if len(fileNames) > 1:
        for i in fileNames:
            os.remove(i)

    deleteOldFiles()

    compileProgram()
    #deleteOldFiles()
