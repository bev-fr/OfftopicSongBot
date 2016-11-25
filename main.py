#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from configparser import ConfigParser
import logging
import re
import yaml


#Bot Configuration
with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

for section in cfg:
    TOKEN = str(cfg['apitoken'])
    subgroups = cfg['subgroups']
    log = str(cfg['log'])


#Compile regex for youtube check
reg = re.compile("^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$")


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(log)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hello! This bot was made for @OfftopicWW and allows members to easily share songs. Just send me a link to a youtube video to submit it.')


def help(bot, update):
    update.message.reply_text('Go to @OfftopicWW or PM @benthecat for help')


def echo(bot, update):
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def urlcheck(url):
    #print('checking url')
    import youtube_dl
    if reg.match(url) is not  None: 
        ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
        with ydl:
            result = ydl.extract_info(url, download=False) # We just want to extract the info
        if 'entries' in result:
            return None
        else:
            #print('it is a video')
            return True
    else:
        #print('regex check failed')
        #print(reg.match(url))
        return None
            
def forward(bot, update):
    uid = str(update.message.from_user.id)
    first = update.message.from_user.first_name
    last =  update.message.from_user.last_name
    cid = str(update.message.chat_id)
    msg = update.message.text
    lmsg = (first, last, uid, cid, msg)
    hy = " - "
    logger.info(hy.join( lmsg))
    
    if update.message.chat_id < 0: return None
    else:
        if urlcheck(update.message.text) is True:
            update.message.reply_text('Submited to @WWotradio')
            seq = (update.message.text, "\nSubmitted by:", first, last)
            s = " "
            for val in subgroups:
                bot.sendMessage(val, s.join( seq ))
        else:
            update.message.reply_text('Please send a valid youtube link')

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, forward))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
