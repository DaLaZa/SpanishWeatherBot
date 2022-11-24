import re
import sqlite3
from .sqLite import check_values, create_initialize_database
from .forecast import *
from .apifunctions import *
from datetime import datetime, timedelta
from .constants import *


# Returns all information
def load_api_information(municipality, hour=None, period=None):
    date_time = datetime.today()
    current_hour = datetime.now().hour

    if period is not None and period.lower() == 'tomorrow':
        date_time = datetime.today() + timedelta(1)
        current_hour = 0

    current_month = datetime.now().month
    snowing_months = {1, 2, 3, 4, 5, 10, 11, 12}
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

    # Call SCHEDULED_PREDICTION's API
    try:
        scheduled_result = get_scheduled_prediction(municipality_cod)
        # Return the position of today's date into json's result
        correct_value_date = check_result_dates(scheduled_result, date_time)
        # Get last actualization and golden hours
        golden_hour_text = golden_hours(scheduled_result, correct_value_date)
        # Get sky scheduled prediction
        try:
            sky_condition = sky_condition_scheduled(scheduled_result, correct_value_date, current_hour, hour)
        except ValueError:
            return NO_DATA_HOUR.upper()
        # Get precipitation probability
        precipitation_probability = probability_precipitation_scheduled(scheduled_result, correct_value_date,
                                                                        current_hour, hour)
        # Get precipitation
        precipitation = precipitation_scheduled(scheduled_result, correct_value_date, current_hour, hour)
        # Get snow probability precipitation only in snowing months
        snow_probability = ""
        if current_month in snowing_months:
            snow_probability = probability_snow_scheduled(scheduled_result, correct_value_date, current_hour, hour)
            snow_probability = f'{snow_probability}{snow_scheduled(scheduled_result, correct_value_date, current_hour, hour)} '

        # Get temperature and thermal sensation temperature
        temperature_values = temperature_scheduled(scheduled_result, correct_value_date, current_hour, hour)
    except ValueError:
        logger.error(f'{DATA_ERROR_MESSAGE} scheduled prediction API', exc_info=True)
        return API_ERROR

    # Get community prediction
    try:
        community_prediction = get_community_prediction(abbreviation)
        # Give a correct format to the community_prediction
        community_prediction = re.split('\\bA\.- \\b', community_prediction)[-1]
        community_prediction = community_prediction.replace("B.- ", "")
    except ValueError:
        logger.error(f'{DATA_ERROR_MESSAGE} community prediction API', exc_info=True)
        return API_ERROR

    # Get province prediction
    try:
        province_prediction = get_daily_provincial_prediction(province_cod)
        # Give a correct format to the province_prediction
        province_prediction = re.split(f'\\b{province.upper()}\\b', province_prediction)[-1]
        province_prediction = re.split(f'\\b{TEMPERATURES}\\b', province_prediction)[0]
    except ValueError:
        logger.error(f'{DATA_ERROR_MESSAGE} province prediction API', exc_info=True)
        return API_ERROR

    return f'{golden_hour_text}{community.upper()}\n{community_prediction}\n{PROVINCE}{province.upper()}' \
           f'{province_prediction}\n{name.upper()}\n{sky_condition}{precipitation_probability}{precipitation}' \
           f'{snow_probability}{temperature_values}'
