import sys
sys.path.append("../..")
from AemetBot.aemet.final_forecast import get_complete_forecast, get_scheduled_forecast
from AemetBot.utils.logger import logger
from AemetBot.telegram_bot.constants_bot import HELP_MESSAGE, ERROR_NUMERIC, TOKEN, \
    ERROR_MUNICIPALITY, MUNICIPALITY_NAME_ERROR, START_MESSAGE, HOUR_PROBLEM
from telegram.ext import *


# Definition: Lets us use the /start command
# Variables:
#   update: Chat information.
#   context: Context
# Created: DAVID LAHUERTA ZAYAS
def start_command(update, context):
    update.message.reply_text(START_MESSAGE)


# Definition: Lets us use the /help command
# Variables:
#   update: Chat information.
#   context: Context
# Created: DAVID LAHUERTA ZAYAS
def help_command(update, context):
    update.message.reply_text(HELP_MESSAGE)


# Definition: Lets us use the /m command, to know tomorrow forecast
# Variables:
#   update: Chat information.
#   context: Context
# Created: DAVID LAHUERTA ZAYAS
# Modified:
#   David Lahuerta: 30-Nov-2022: Add first and second hour to show ranges of hours
def tomorrow_command(update, context):
    # Get basic info of the incoming message
    text = str(update.message.text)

    # Print a log for debugging
    print(f'User ({update.message.chat.id}) says: "{text}"')
    logger.debug(f'User ({update.message.chat.id}) says: "{text}"')
    try:
        municipality, first_hour, second_hour = handle_response(update, text)
    except ValueError:
        return None

    if first_hour is None:
        result = get_complete_forecast(municipality[2:], "tomorrow")
    else:
        result = get_scheduled_forecast(municipality[2:], first_hour, second_hour, "tomorrow")

    # Reply normal if the message is in private
    update.message.reply_text(result)


# Definition: Handle the information send by the user, to get the municipality and hours
# Variables:
#   update: Chat information.
#   args: Text sent by the user
# Created: DAVID LAHUERTA ZAYAS
# Modified:
#   David Lahuerta: 30-Nov-2022: Add first and second hour to show ranges of hours
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
        first_hour = hour.split("-")[0].strip()
        first_hour = first_hour.split(":")[0]

        if first_hour == '':
            return municipality, None, None
        if not first_hour.isnumeric():
            update.message.reply_text(ERROR_NUMERIC)
            return []
    except IndexError:
        return municipality, None, None

    try:
        second_hour = hour.split("-")[1].strip()
        second_hour = second_hour.split(":")[0]

        if second_hour == '':
            return municipality, int(first_hour), None
        if not second_hour.isnumeric():
            update.message.reply_text(ERROR_NUMERIC)
            return []
    except IndexError:
        return municipality, int(first_hour), None

    if int(first_hour) > 24 or int(second_hour) > 24:
        update.message.reply_text(HOUR_PROBLEM)
        return []

    if int(first_hour) == 24:
        first_hour = 23
    if int(second_hour) == 24:
        second_hour = 23

    hours = [int(first_hour), int(second_hour)]
    hours.sort()
    return municipality, hours[0], hours[1]


# Definition: Handle the bot messages
# Variables:
#   update: Chat information.
#   context: Context
# Created: DAVID LAHUERTA ZAYAS
def handle_message(update, context):
    # Get basic info of the incoming message
    text = str(update.message.text)

    # Print a log for debugging
    logger.debug(f'User ({update.message.chat.id}) says: "{text}"')
    try:
        municipality, first_hour, second_hour = handle_response(update, text)
    except ValueError:
        return None

    if first_hour is None:
        result = get_complete_forecast(municipality)
    else:
        result = get_scheduled_forecast(municipality, first_hour, second_hour)

    # Reply normal if the message is in private
    update.message.reply_text(result)


# Definition: Log errors
# Variables:
#   update: Chat information.
#   context: Context
# Created: DAVID LAHUERTA ZAYAS
def error(update, context):
    logger.debug(f'Update {update} caused error {context.error}')


# Definition: MAIN - Run the program
# Created: DAVID LAHUERTA ZAYAS
# Modified:
#   David Lahuerta: 30-Nov-2022: Change tomorrow_comand set m instead of tomorrow
if __name__ == '__main__':
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('m', tomorrow_command))

    # Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Log all errors
    dp.add_error_handler(error)

    # Run the bot
    updater.start_polling(1.0)
    updater.idle()
