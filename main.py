from telegram.ext import * 
from telegram import *
import os
import multiprocessing
from flask import Flask
from threading import Thread
import json
from BotModules import FlaskKeepAlive as FlaskKeepAlive
from BotModules import bothelp as bothelp
from BotModules import Heart as Heart

# Reading Config Data
with open('config.json') as json_file:
    print('\n[+] : Reading config Data')
    ConfigData = json.load(json_file)
    print('[√] : Config Data read successfully\n')
 
    

class Starting():
    def __init__(self):
        self.initiliaze = Heart.News()
    
    def LGR(self, CommandToReplace, RecievedMsg, context, update, MessageID):
        self.initiliaze.LGR(CommandToReplace, RecievedMsg, context, update, MessageID)
    
    def RFC(self, CommandToReplace, RecievedMsg, context, update, MessageID):
        self.initiliaze.RFC(CommandToReplace, RecievedMsg, context, update, MessageID)
start = Starting()

def BotHelp(update, context):
    HelpMessage = bothelp.BotHelpMessage(ConfigData['COMMANDS'])

    ChatID = update.message.chat_id
    context.bot.sendMessage(chat_id = ChatID, text = HelpMessage, parse_mode = ParseMode.HTML)


def News_Command(update, context):

    RecievedMsg = update.message.text
    MessageID = update.message.message_id

    CommandToReplace = ConfigData['COMMANDS']['News']
    start.LGR(CommandToReplace, RecievedMsg, context, update, MessageID)
    start.RFC(CommandToReplace, RecievedMsg, context, update, MessageID)


def BotMain(seconds):

    print('\n[+] : Starting Bot')

    if (ConfigData['Deploy'] == '1'):
        my_secret = os.environ['API_KEY']
    else:
        my_secret = ConfigData['API_KEY']

    updater = Updater(my_secret, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler(f"{ConfigData['COMMANDS']['News']}", News_Command))
    dp.add_handler(CommandHandler(f"{ConfigData['COMMANDS']['Help']}", BotHelp))

    updater.start_polling()
    print("\n[√] BOT STARTED SUCCESSFULLY [√]\n")
    updater.idle()

# Running multithreads
#BotMain('1')
# p1 = multiprocessing.Process(target=BotMain, args=[1])
# p2 = multiprocessing.Process(target=FlaskKeepAlive.FlaskApp, args=[1])

# if __name__ == '__main__':
#     p1.start()
#     p2.start()
    
if __name__ == '__main__':

    # p1 = multiprocessing.Process(target=BotMain, args=[1])
    # p1.start()
    # p2 = multiprocessing.Process(target=FlaskKeepAlive.FlaskApp, args=[1])
    # p2.start()

    BotMain('1')
