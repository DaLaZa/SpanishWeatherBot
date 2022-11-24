import sys
sys.path.append('..')
sys.path.append('../..')

from aemet.final_forecast import load_api_information
from utils.logger import logger
from telegram_bot.constants_bot import HELP_MESSAGE, ERROR_NUMERIC, TOKEN, \
    ERROR_MUNICIPALITY, MUNICIPALITY_NAME_ERROR, START_MESSAGE, HOUR_PROBLEM
from telegram.ext import *


# Lets us use the /start command
def start_command(update, context):
    update.message.reply_text(START_MESSAGE)


# Lets us use the /help command
def help_command(update, context):
    update.message.reply_text(HELP_MESSAGE)


# Lets us use the /tomorrow command
def tomorrow_command(update, context):
    # Get basic info of the incoming message
    text = str(update.message.text)

    # Print a log for debugging
    print(f'User ({update.message.chat.id}) says: "{text}"')
    logger.debug(f'User ({update.message.chat.id}) says: "{text}"')
    try:
        municipality, hour = handle_response(update, text)
    except ValueError:
        return None

    result = load_api_information(municipality, hour, text[1:8])
    # Reply normal if the message is in private
    update.message.reply_text(result)


def handle_response(update, args):
    args = args.split(";")

    try:
        municipality = args[0]
        if municipality.isnumeric():
            update.message.reply_text(ERROR_MUNICIPALITY)
            return ValueError
    except IndexError:
        raise ValueError(MUNICIPALITY_NAME_ERROR)

    try:
        hour = args[1].strip()
        hour = hour.split(":")[0]
    except IndexError:
        hour = None

    if hour is not None:
        if hour == '':
            return municipality, None
        if not hour.isnumeric():
            update.message.reply_text(ERROR_NUMERIC)
            return []

        hour = int(hour)

    return municipality, hour


def handle_message(update, context):
    # Get basic info of the incoming message
    text = str(update.message.text)

    # Print a log for debugging
    logger.debug(f'User ({update.message.chat.id}) says: "{text}"')
    try:
        municipality, hour = handle_response(update, text)
    except ValueError:
        return None

    result = load_api_information(municipality, hour)
    # Reply normal if the message is in private
    update.message.reply_text(result)


# Log errors
def error(update, context):
    logger.debug(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('tomorrow', tomorrow_command))

    # Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Log all errors
    dp.add_error_handler(error)

    # Run the bot
    updater.start_polling(1.0)
    updater.idle()
