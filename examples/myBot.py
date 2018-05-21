#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.

First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY = range(2)

reply_keyboard = [['Validate Code', 'Help'],
                  ['Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(bot, update):
    update.message.reply_text(
        "Hi! My name is Chaince Bot, Please choose a service",
        reply_markup=markup)

    return CHOOSING


def Validate_choice(bot, update):
    update.message.reply_text('Please input your code')

    return TYPING_REPLY


def help_choice(bot, update):
    update.message.reply_text('Please contact @Chaince for help')

    return CHOOSING


def received_code(bot, update, user_data):
    text = update.message.text
    
    if('code' in user_data):
        update.message.reply_text("You have already validated this code!",reply_markup=markup)
        return CHOOSING

    update.message.reply_text("This is what you already told me:"
                              "{}\n"
                              "Let me check this code......".format(
                                  text),reply_markup=markup)
    if(validate_code(text)):
        user_data['code'] = text
        update.message.reply_text("Congratulations! This code:"
                              "{}\n"
                              "is Valid".format(
                                  text),reply_markup=markup)
        return CHOOSING
    else:
        update.message.reply_text("Sorry, This code:"
                              "{}\n"
                              "is not Valid".format(
                                  text),reply_markup=markup)
        return CHOOSING

def validate_code(code):
    if(len(code) > 5):
        return True
    return False
  

def done(bot, update, user_data):
    if 'code' in user_data:
        del user_data['code']

    update.message.reply_text("Thanks for using Chaince Bot")

    user_data.clear()
    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("609834587:AAHmp4q7Qz9_m7EU1YWA_klHu4im3tPN5Oc")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [RegexHandler('^(Validate Code)$',
                                    Validate_choice,
                                    pass_user_data=False),
                       RegexHandler('^Help$',
                                    help_choice),
                       ],
            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_code,
                                          pass_user_data=True),
                           ],
        },

        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
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
