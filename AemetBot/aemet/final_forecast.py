import re
import sqlite3
from .sqLite import check_values, create_initialize_database
from .forecast import *
from .apifunctions import *
from datetime import datetime, timedelta
from .constants import *

current_month = datetime.now().month
snowing_months = {1, 2, 3, 4, 5, 10, 11, 12}


# Definition: Returns all scheduled information
# Variables:
#   municipality: Selected municipality by the user.
#   hour: Selected hour by the user.
#   period: Selected period by the user.
# Created: DAVID LAHUERTA ZAYAS
def get_scheduled_info(municipality_cod, date_time, current_hour, first_hour=None, second_hour=None):
    # Call SCHEDULED_PREDICTION's API
    try:
        scheduled_result = get_scheduled_prediction(municipality_cod)
        # Return the position of today's date into json's result
        correct_value_date = check_result_dates(scheduled_result, date_time)
        # Get last actualization and golden hours
        golden_hour_text = golden_hours(scheduled_result, correct_value_date)
        # Get sky scheduled prediction
        try:
            sky_condition = sky_condition_scheduled(scheduled_result, correct_value_date, current_hour, first_hour,
                                                    second_hour)
        except ValueError:
            return []
        # Get precipitation probability
        precipitation_probability = probability_precipitation_scheduled(scheduled_result, correct_value_date,
                                                                        current_hour, first_hour, second_hour)
        # Get precipitation
        precipitation = precipitation_scheduled(scheduled_result, correct_value_date, current_hour, first_hour,
                                                second_hour)
        # Get snow probability precipitation only in snowing months
        snow_probability = ""
        if current_month in snowing_months:
            snow_probability = probability_snow_scheduled(scheduled_result, correct_value_date, current_hour,
                                                          first_hour, second_hour)
            snow_precipitation = snow_scheduled(scheduled_result, correct_value_date, current_hour, first_hour,
                                                second_hour)
            snow_probability = f'{snow_probability}{snow_precipitation}'

        # Get temperature and thermal sensation temperature
        temperature_values = temperature_scheduled(scheduled_result, correct_value_date, current_hour, first_hour,
                                                   second_hour)
    except ValueError:
        logger.error(f'{DATA_ERROR_MESSAGE} scheduled prediction API', exc_info=True)
        return API_ERROR

    return golden_hour_text, sky_condition, precipitation_probability, precipitation, snow_probability, \
           temperature_values


# Definition: Returns all information
# Variables:
#   municipality: Selected municipality by the user.
#   hour: Selected hour by the user.
#   period: Selected period by the user.
# Created: DAVID LAHUERTA ZAYAS
# Modified:
#   David Lahuerta: 29-Nov-2022: Add get_scheduled_info to get the scheduled prediction
#   David Lahuerta: 13-Dec-2022: Get the correct community and province prediction
def get_complete_forecast(municipality, period=None):
    date_today_format = "%Y-%m-%d %H:%M:%S.%f"
    date_time = datetime.today()
    yesterday_time = datetime.today() - timedelta(1)
    tomorrow_time = datetime.today() + timedelta(1)
    yesterday = str(yesterday_time.strptime(str(yesterday_time), date_today_format).strftime("%Y-%m-%d"))
    today = str(date_time.strptime(str(date_time), date_today_format).strftime("%Y-%m-%d"))
    tomorrow = str(tomorrow_time.strptime(str(tomorrow_time), date_today_format).strftime("%Y-%m-%d"))
    current_hour = datetime.now().hour

    if period is not None and period.lower() == 'tomorrow':
        date_time = datetime.today() + timedelta(1)
        current_hour = 0

    # Get municipality_cod (ex.: Teruel is 44216) and province_cod (ex.: Teruel is 44)
    try:
        municipality_cod, province_cod, name = get_all_xls_codes(municipality)
    except ValueError:
        logger.error(f'{DATA_ERROR_MESSAGE} city: {municipality}', exc_info=True)
        return VALUE_ERROR

    # Open connection
    try:
        conn = sqlite3.connect(DATA_BASE_NAME)
        check_values(conn)
    except sqlite3.OperationalError:
        create_initialize_database()

    # Get province name
    try:
        province = get_province_name(province_cod, conn)
    except ValueError:
        logger.error(f'{DATA_ERROR_MESSAGE} province name: {province_cod}', exc_info=True)
    # Get community name
    try:
        community = get_community_name(province_cod, conn)
    except ValueError:
        logger.error(f'{DATA_ERROR_MESSAGE} community name: {province_cod}', exc_info=True)
    # Get community abbreviation
    try:
        abbreviation = get_community_code(province_cod, conn)
    except ValueError:
        logger.error(f'{DATA_ERROR_MESSAGE} community abbreviation: {province_cod}', exc_info=True)
    # Close the connection
    conn.close()

    try:
        golden_hour_text, sky_condition, precipitation_probability, precipitation, snow_probability, temperature_values\
            = get_scheduled_info(municipality_cod, date_time, current_hour, None, None)
    except ValueError:
        return NO_DATA_HOUR.upper()

    # Get community prediction
    if period is not None and period.lower() == 'tomorrow':
        try:
            community_prediction = get_community_prediction(abbreviation, today)
        except ValueError:
            logger.error(f'{DATA_ERROR_MESSAGE} province prediction API', exc_info=True)
            return API_ERROR
    else:
        try:
            community_prediction = get_community_prediction(abbreviation, yesterday)
        except ValueError:
            logger.error(f'{DATA_ERROR_MESSAGE} province prediction API', exc_info=True)
            return API_ERROR
    try:
        # Give a correct format to the community_prediction
        community_prediction = re.split('\\bA\.- \\b', community_prediction)[-1]
        community_prediction = community_prediction.replace("B.- ", "")
    except ValueError:
        logger.error(f'{DATA_ERROR_MESSAGE} community prediction API', exc_info=True)
        return API_ERROR

    # Get province prediction
    if period is not None and period.lower() == 'tomorrow':
        try:
            province_prediction = get_tomorrow_daily_provincial_prediction(province_cod)
        except ValueError:
            logger.error(f'{DATA_ERROR_MESSAGE} province prediction API', exc_info=True)
            return API_ERROR
    else:
        try:
            province_prediction = get_daily_provincial_prediction(province_cod, today)
        except ValueError:
            logger.error(f'{DATA_ERROR_MESSAGE} province prediction API', exc_info=True)
            return API_ERROR
    try:
        # Give a correct format to the province_prediction
        province_prediction = re.split(f'\\b{province.upper()}\\b', province_prediction)[-1]
        province_prediction = re.split(f'\\b{TEMPERATURES}\\b', province_prediction)[0]
    except ValueError:
        logger.error(f'{DATA_ERROR_MESSAGE} province prediction API', exc_info=True)
        return API_ERROR

    return f'{golden_hour_text}{community.upper()}\n{community_prediction}\n{PROVINCE}{province.upper()}' \
           f'{province_prediction}\n{name.upper()}\n{sky_condition}{precipitation_probability}{precipitation}' \
           f'{snow_probability}{temperature_values}'


# Definition: Returns only the scheduled information
# Variables:
#   municipality: Selected municipality by the user.
#   hour: Selected hour by the user.
#   period: Selected period by the user.
# Created: DAVID LAHUERTA ZAYAS
def get_scheduled_forecast(municipality, first_hour, second_hour=None, period=None):
    date_time = datetime.today()
    current_hour = datetime.now().hour

    if period is not None and period.lower() == 'tomorrow':
        date_time = datetime.today() + timedelta(1)
        current_hour = 0

    # Get municipality_cod (ex.: Teruel is 44216) and province_cod (ex.: Teruel is 44)
    try:
        municipality_cod, province_cod, name = get_all_xls_codes(municipality)
    except ValueError:
        logger.error(f'{DATA_ERROR_MESSAGE} city: {municipality}', exc_info=True)
        return VALUE_ERROR

    try:
        golden_hour_text, sky_condition, precipitation_probability, precipitation, snow_probability, temperature_values\
            = get_scheduled_info(municipality_cod, date_time, current_hour, first_hour, second_hour)
    except ValueError:
        return NO_DATA_HOUR.upper()

    return f'{golden_hour_text}{name.upper()}\n{sky_condition}{precipitation_probability}{precipitation}' \
           f'{snow_probability}{temperature_values}'
