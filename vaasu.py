#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective paces.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import os
import logging
from dotenv import load_dotenv

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

GETID, PASS, LOCATION, BIO = range(4)

load_dotenv()

def start(update, context):

    update.message.reply_text(
        'Hi! My name is Vaassu Bot. I will get all attendence details, '
        'so that you guys can bunk class more often 😜.\n\n'
        # 'Type /login to login to get your attendence.'
        'Type /stop to stop me😥',
        reply_markup=ReplyKeyboardRemove())

    return GETID


def getid(update, context):
    user = update.message.from_user
    logger.info("User %s started the bot.", user.first_name)
    update.message.reply_text('please enter your id ')

    return PASS


def getpass(update, context):
    user = update.message.from_user
    # photo_file = update.message.photo[-1].get_file()
    # photo_file.download('user_photo.jpg')
    logger.info("ID of %s: %s", user.first_name, user.message.text)
    update.message.reply_text('Gorgeous! Now, send me your location please, '
                              'or send /skip if you don\'t want to.')

    return LOCATION


# def skip_photo(update, context):
#     user = update.message.from_user
#     logger.info("User %s did not send a photo.", user.first_name)
#     update.message.reply_text('I bet you look great! Now, send me your location please, '
#                               'or send /skip.')

#     return LOCATION


def location(update, context):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Maybe I can visit you sometime! '
                              'At last, tell me something about yourself.')

    return BIO


# def skip_location(update, context):
#     user = update.message.from_user
#     logger.info("User %s did not send a location.", user.first_name)
#     update.message.reply_text('You seem a bit paranoid! '
#                               'At last, tell me something about yourself.')

#     return BIO


# def bio(update, context):
#     user = update.message.from_user
#     logger.info("Bio of %s: %s", user.first_name, update.message.text)
#     update.message.reply_text('Thank you! I hope we can talk again some day.')

#     return ConversationHandler.END

def stop(update, context):
    user = update.message.from_user
    logger.info("User %s stop its working...", user.first_name)
    update.message.reply_text(
        'This bot is created by @fossersvast.'
        'Show some love when you see us ❤. May be with some treat.😊'
        'Bye! I hope we can meet again at Iraani.',
        reply_markup=ReplyKeyboardRemove())

    return 

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(os.getenv('BOT_TOKEN'), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            GETID: [MessageHandler(Filters.text, getid)],

            PASS: [MessageHandler(Filters.text, getpass)],

            LOCATION: [MessageHandler(Filters.location, location)],

            # BIO: [MessageHandler(Filters.text, bio)],

            # ABOUT: [MessageHandler(Filters.text, about),
                    # CommandHandler('about',about)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
