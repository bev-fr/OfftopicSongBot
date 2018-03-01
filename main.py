#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This program is dedicated to the public domain under the CC0 license.

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from configparser import ConfigParser
import logging
import yaml
import youtube_dl
import re

#Compile regex for youtube check
reg = re.compile("^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$")

           

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

# Enable logging
logging.basicConfig(format= u'%(asctime)-s %(levelname)s [%(name)s]: %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(log)
formatter = logging.Formatter(u'%(asctime)-s %(levelname)s [%(name)s]: %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hello! This bot was made for @OfftopicWW and allows members to easily share songs. Just send me a link to a youtube video to submit it.')


def help(bot, update):
    update.message.reply_text('Go to @OfftopicWW or PM @benthecat for help')


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))
           
def log_message(update):
    uid = str(update.message.from_user.id)
    first = (update.message.from_user.first_name)
    last =  (update.message.from_user.last_name)
    cid = str(update.message.chat_id)
    msg = update.message.text
    lmsg = (first, last, uid, cid, msg)
    hy = " - "
    logger.info(hy.join( lmsg))

def urlcheck(url):
    if reg.match(url) is not None: 
        ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
        with ydl:
            try:
                result = ydl.extract_info(url, download=False) 
            except youtube_dl.utils.DownloadError:
                return False

        if 'entries' in result:
            return False
        else:
            return True
    else:
        return False

def forward(bot, update):
    logger.info('Received Message')
    if update.message.chat_id < 0:
        logger.info('Received in Group')
        return None
    elif update.message.from_user.id in blocked: 
        logger.info('Blocked from posting')
        return None
    else:
        log_message(update)
        if urlcheck(update.message.text) is True:
            logger.info('Submitted link')
            update.message.reply_text('Submited to @WWotradio')
            first = (update.message.from_user.first_name)
            last =  (update.message.from_user.last_name)
            seq = (update.message.text, "\nSubmitted by:", first, last)
            s = " ".join(seq)
            for val in subgroups:
                bot.sendMessage(val, s)
#        elif update.message.video:
#            logger.info('Submitted video')
#            update.message.reply_text('Submitted to @WWotradio')
#            first = (update.message.from_user.first_name)
#            last = (update.message.from_user.last_name)
#            seq = ("Submitted by:", first, last)
#            if update.message.caption:
#                seq = (update.message.caption, "\nSubmitted by:", first, last)
#            s = " ".join(seq)
#            for val in subgroups:
#                bot.sendVideo(chat_id = val, video = update.message.video.file_id, caption = s)
#        elif update.message.audio:
#            logger.info('Submitted audio')
#            update.message.reply_text('Submitted to @WWotradio')
#            first = (update.message.from_user.first_name)
#            last = (update.message.from_user.last_name)
#            seq = ("Submitted by:", first, last)
#            if update.message.caption:
#                seq = (update.message.caption, "\nSubmitted by:", first, last)
#            s = " ".join(seq)
#            for val in subgroups:
#                bot.sendAudio(chat_id = val, audio = update.message.audio.file_id, caption = s)
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
    dp.add_handler(MessageHandler(Filters.text, forward))# | Filters.audio | Filters.video, forward))

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
