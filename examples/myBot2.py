#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.

This program is dedicated to the public domain under the CC0 license.

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
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text(update.message.text)


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update,user_data):
    """Echo the user message."""
    text = update.message.text
    if("valid" in text):
        if(text[:5] == "valid"):
            code = text[5:]
            code = code.strip()
            if(user_data.has_key(code)):
                code_validate = "not Valid"
                if(user_data[code]):
                    code_validate = "Valid"
                update.message.reply_text('You have already sent this code:%s, this is %s, please do not send this again'%(code,code_validate))
            else:
                if(validateCode(code)):
                    user_data[code] = True
                    update.message.reply_text('Congratulations! this code: %s is valid!'%(code))
                else:
                    user_data[code] = False
                    update.message.reply_text('Sorry! this code: %s is not valid!'%(code))

def validateCode(code):
    if(len(code) > 5):
        return True
    else:
        return False

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    token = "609834587:AAHmp4q7Qz9_m7EU1YWA_klHu4im3tPN5Oc"
    token = "553719325:AAHY_RRZnny-t6xnYQpglJrHdfTS6T0YjiE"
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo,pass_user_data=True))

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
