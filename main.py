#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This program is dedicated to the public domain under the CC0 license.

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from configparser import ConfigParser
import logging
import re
import yaml
import youtube_dl


#Bot Configuration
with open("config.yml", 'r') as configfile:
    cfg = yaml.load(configfile)

for section in cfg:
    TOKEN = str(cfg['apitoken'])
    subgroups = cfg['subgroups']
    log = str(cfg['log'])


#Blocked Users
with open("blocked.yml", 'r') as blockedfile:
    busers = yaml.load(blockedfile)

for section in cfg:
    blocked = busers['blockedusers']


#Compile regex for youtube check
reg = re.compile("^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$")


# Enable logging
logging.basicConfig(format= u'%(asctime)-s %(levelname)s [%(name)s]: %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(log)
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
    logger.debug('Checking video')
    if reg.match(url) is not  None: 
        ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
        with ydl:
            result = ydl.extract_info(url, download=False) # We just want to extract the info
        if 'entries' in result:
            return None
        else:
            return True
    else:
        return None
           
def log_message(update):
    uid = str(update.message.from_user.id)
    first = (update.message.from_user.first_name)
    last =  (update.message.from_user.last_name)
    cid = str(update.message.chat_id)
    msg = update.message.text
    lmsg = (first, last, uid, cid, msg)
    hy = " - "
    logger.info(hy.join( lmsg))


def forward(bot, update):
    log_message(update)
    if update.message.chat_id < 0: return None
    elif update.message.from_user.id in blocked: 
        logger.info('Blocked from posting')
        return None
    else:
        if urlcheck(update.message.text) is True:
            logger.info('Submitted')
            update.message.reply_text('Submited to @WWotradio')
            first = (update.message.from_user.first_name)
            last =  (update.message.from_user.last_name)
            seq = (update.message.text, "\nSubmitted by:", first, last)
            s = " "
            for val in subgroups:
                bot.sendMessage(val, s.join( seq ))
        else:
            logger.info('Invalid link')
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
