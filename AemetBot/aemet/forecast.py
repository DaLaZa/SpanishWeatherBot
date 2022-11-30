from datetime import datetime
from .constants import *


# Definition: Checks the JSON file dates to return the correct one.
# Variables:
#   result: Aemet API information.
#   date_time: Current datetime.
# Created: DAVID LAHUERTA ZAYAS
def check_result_dates(result, date_time):
    date_today_format = "%Y-%m-%d %H:%M:%S.%f"
    date_today = str(datetime.strptime(str(date_time), date_today_format).strftime("%d-%b-%Y"))

    for value in range(4):
        date_result = result[0]["prediccion"]["dia"][value]["fecha"]
        date_json = str(datetime.strptime(date_result, DATA_TYPE).strftime("%d-%b-%Y"))

        if date_today == date_json:
            return value
    return 0


# Definition: Get the last load values and golden hours.
# Variables:
#   scheduled_result: Aemet API information.
#   correct_value_date: Correct date position in JSON file.
# Created: DAVID LAHUERTA ZAYAS
def golden_hours(scheduled_result, correct_value_date):
    sunrise = scheduled_result[0]["prediccion"]["dia"][correct_value_date]["orto"]
    sunset = scheduled_result[0]["prediccion"]["dia"][correct_value_date]["ocaso"]
    elaboration = scheduled_result[0]["elaborado"]
    date = str(datetime.strptime(elaboration, DATA_TYPE).strftime("%d-%b-%Y; %H:%M:%S"))

    return f'ULTIMA ACTUALIZACION: {date}\nAMANECE:  {sunrise}\nANOCHECE: {sunset}\n\n'


# Definition: Get the sky condition
# Variables:
#   scheduled_result: Aemet API information.
#   correct_value_date: Correct date position in JSON file.
#   current_hour: Current hour, it used to show the info from that hour when the user doesn't specify an hour.
#   hour: Selected hour by the user.
# Created: DAVID LAHUERTA ZAYAS
# Modified:
#   David Lahuerta: 29-Nov-2022: Add first and second hour to show ranges of hours
def sky_condition_scheduled(scheduled_result, correct_value_date, current_hour, first_hour=None, second_hour=None):
    ranges = {element["periodo"]: element["descripcion"] for element in
              scheduled_result[0]["prediccion"]["dia"][correct_value_date]["estadoCielo"]}

    sky_condition = SKY_CONDITION
    sky_condition_found = False
    if first_hour is None:
        for key, value in ranges.items():
            if int(key) >= current_hour:
                sky_condition_found = True
                sky_condition = f'{sky_condition}{key}h: {value}\n'
    elif second_hour is None:
        for key, value in ranges.items():
            if first_hour < int(key):
                raise ValueError
            elif first_hour == int(key):
                sky_condition_found = True
                sky_condition = f'{sky_condition}{key}h: {value}\n\n'
                break
    else:
        for key, value in ranges.items():
            if first_hour <= int(key) <= second_hour:
                sky_condition_found = True
                sky_condition = f'{sky_condition}{key}h: {value}\n'

    if not sky_condition_found:
        raise ValueError

    return sky_condition


# Definition: Get the probability of precipitation
# Variables:
#   scheduled_result: Aemet API information.
#   correct_value_date: Correct date position in JSON file.
#   current_hour: Current hour, it used to show the info from that hour when the user doesn't specify an hour.
#   hour: Selected hour by the user.
# Created: DAVID LAHUERTA ZAYAS
# Modified:
#   David Lahuerta: 29-Nov-2022: Add first and second hour to show ranges of hours
def probability_precipitation_scheduled(scheduled_result, correct_value_date, current_hour,
                                        first_hour=None, second_hour=None):
    ranges = {element["periodo"]: element["value"] for element in
              scheduled_result[0]["prediccion"]["dia"][correct_value_date]["probPrecipitacion"]}

    precipitation = PRECIPITATION_PROBABILITY
    check_hour = False

    if first_hour is None:
        for key, value in ranges.items():
            if current_hour <= int(key[0:2]):
                check_hour = True
                precipitation = f'{precipitation}Entre las: {key[0:2]}h-{key[2:4]}h: {str(value)}%\n'
            if int(key[2:4]) == 1 and check_hour is False:
                if current_hour <= 24:
                    precipitation = f'{precipitation}Entre las: {key[0:2]}h-{key[2:4]}h: {str(value)}%\n'
    elif second_hour is None:
        for key, value in ranges.items():
            if int(key[2:4]) < int(key[0:2]):
                real_hour = 24
            else:
                real_hour = int(key[2:4])
            if first_hour in range(int(key[0:2]), real_hour):
                precipitation = f'{precipitation}Entre las: {key[0:2]}h-{key[2:4]}h: {str(value)}%\n\n'
                break
    else:
        for key, value in ranges.items():
            if first_hour <= int(key[0:2]) <= second_hour:
                check_hour = True
                precipitation = f'{precipitation}Entre las: {key[0:2]}h-{key[2:4]}h: {str(value)}%\n'
            if int(key[2:4]) == 1 and check_hour is False:
                if second_hour <= 24:
                    precipitation = f'{precipitation}Entre las: {key[0:2]}h-{key[2:4]}h: {str(value)}%\n'

    return precipitation


# Definition: Get the precipitation hours
# Variables:
#   scheduled_result: Aemet API information.
#   correct_value_date: Correct date position in JSON file.
#   current_hour: Current hour, it used to show the info from that hour when the user doesn't specify an hour.
#   hour: Selected hour by the user.
# Created: DAVID LAHUERTA ZAYAS
# Modified:
#   David Lahuerta: 29-Nov-2022: Add first and second hour to show ranges of hours
def precipitation_scheduled(scheduled_result, correct_value_date, current_hour, first_hour=None, second_hour=None):
    ranges = {element["periodo"]: element["value"] for element in
              scheduled_result[0]["prediccion"]["dia"][correct_value_date]["precipitacion"]}

    precipitation = PRECIPITATION

    if first_hour is None:
        for key, value in ranges.items():
            if int(key) >= current_hour:
                precipitation += f'{key}h: {value} (mm)\n'
    elif second_hour is None:
        for key, value in ranges.items():
            if first_hour < int(key):
                return ""
            elif first_hour == int(key):
                precipitation += f'{key}h: {value} (mm)\n\n'
                break
    else:
        for key, value in ranges.items():
            if first_hour <= int(key) <= second_hour:
                precipitation += f'{key}h: {value} (mm)\n'

    return precipitation


# Definition: Get the probability of snowing
# Variables:
#   scheduled_result: Aemet API information.
#   correct_value_date: Correct date position in JSON file.
#   current_hour: Current hour, it used to show the info from that hour when the user doesn't specify an hour.
#   hour: Selected hour by the user.
# Created: DAVID LAHUERTA ZAYAS
# Modified:
#   David Lahuerta: 29-Nov-2022: Add first and second hour to show ranges of hours
def probability_snow_scheduled(scheduled_result, correct_value_date, current_hour, first_hour=None, second_hour=None):
    ranges = {element["periodo"]: element["value"] for element in
              scheduled_result[0]["prediccion"]["dia"][correct_value_date]["probNieve"]}

    snow = SNOW_PROBABILITY
    check_hour = False

    if first_hour is None:
        for key, value in ranges.items():
            if current_hour <= int(key[0:2]):
                check_hour = True
                snow = f'{snow}Entre las: {key[0:2]}h-{key[2:4]}h: {str(value)}%\n'
            if int(key[2:4]) == 1 and check_hour is False:
                if current_hour <= 24:
                    snow = f'{snow}Entre las: {key[0:2]}h-{key[2:4]}h: {str(value)}%\n'
    elif second_hour is None:
        for key, value in ranges.items():
            if int(key[2:4]) < int(key[0:2]):
                real_hour = 24
            else:
                real_hour = int(key[2:4])
            if first_hour in range(int(key[0:2]), real_hour):
                snow = f'{snow}Entre las: {key[0:2]}h-{key[2:4]}h: {str(value)}%\n\n'
                break
    else:
        for key, value in ranges.items():
            if first_hour <= int(key[0:2]) <= second_hour:
                check_hour = True
                snow = f'{snow}Entre las: {key[0:2]}h-{key[2:4]}h: {str(value)}%\n'
            if int(key[2:4]) == 1 and check_hour is False:
                if second_hour <= 24:
                    snow = f'{snow}Entre las: {key[0:2]}h-{key[2:4]}h: {str(value)}%\n'

    return snow


# Definition: Get the snow precipitation
# Variables:
#   scheduled_result: Aemet API information.
#   correct_value_date: Correct date position in JSON file.
#   current_hour: Current hour, it used to show the info from that hour when the user doesn't specify an hour.
#   hour: Selected hour by the user.
# Created: DAVID LAHUERTA ZAYAS
# Modified:
#   David Lahuerta: 29-Nov-2022: Add first and second hour to show ranges of hours
def snow_scheduled(scheduled_result, correct_value_date, current_hour, first_hour=None, second_hour=None):
    ranges = {element["periodo"]: element["value"] for element in
              scheduled_result[0]["prediccion"]["dia"][correct_value_date]["nieve"]}

    snow = SNOW

    if first_hour is None:
        for key, value in ranges.items():
            if int(key) >= current_hour:
                snow = f'{snow}{key}h: {value} (mm)\n'
    elif second_hour is None:
        for key, value in ranges.items():
            if first_hour == int(key):
                snow = f'{snow}{key}h: {value} (mm)\n\n'
                break
    else:
        for key, value in ranges.items():
            if first_hour <= int(key) <= second_hour:
                snow = f'{snow}{key}h: {value} (mm)\n'

    return snow


# Definition: Get the temperature and thermal sensation
# Variables:
#   scheduled_result: Aemet API information.
#   correct_value_date: Correct date position in JSON file.
#   current_hour: Current hour, it used to show the info from that hour when the user doesn't specify an hour.
#   hour: Selected hour by the user.
# Created: DAVID LAHUERTA ZAYAS
# Modified:
#   David Lahuerta: 29-Nov-2022: Add first and second hour to show ranges of hours
def temperature_scheduled(scheduled_result, correct_value_date, current_hour, first_hour=None, second_hour=None):
    current_temperature = {element["periodo"]: element["value"] for element in
                           scheduled_result[0]["prediccion"]["dia"][correct_value_date]["temperatura"]}

    thermal_sensation = {element["periodo"]: element["value"] for element in
                         scheduled_result[0]["prediccion"]["dia"][correct_value_date]["sensTermica"]}

    temperature_values = ""
    thermal_temperature = ""
    final_temperature = TEMPERATURE

    if first_hour is None:
        for key_temperature, value_temperature in current_temperature.items():
            if int(key_temperature) >= current_hour:
                temperature_values = f'{temperature_values}{key_temperature}h: Temperatura: {value_temperature}ºC;'

        for key, value in thermal_sensation.items():
            if int(key) >= current_hour:
                thermal_temperature = f'{thermal_temperature} Sensacion termica: {value}ºC\n'

        temperature_values = temperature_values.split(";")
        thermal_temperature = thermal_temperature.split("\n")

        for i in range(len(temperature_values) - 1):
            final_temperature = f'{final_temperature}{temperature_values[i]};{thermal_temperature[i]}\n'

    elif second_hour is None:
        for key_temperature, value_temperature in current_temperature.items():
            if first_hour == int(key_temperature):
                final_temperature = f'{final_temperature}{key_temperature}h: Temperatura: {value_temperature}ºC;'
                break

        for key, value in thermal_sensation.items():
            if first_hour == int(key):
                final_temperature = f'{final_temperature} Sensacion termica: {value}ºC\n\n'
                break
    else:
        for key_temperature, value_temperature in current_temperature.items():
            if first_hour <= int(key_temperature) <= second_hour:
                temperature_values = f'{temperature_values}{key_temperature}h: Temperatura: {value_temperature}ºC;'

        for key, value in thermal_sensation.items():
            if first_hour <= int(key) <= second_hour:
                thermal_temperature = f'{thermal_temperature} Sensacion termica: {value}ºC\n'

        temperature_values = temperature_values.split(";")
        thermal_temperature = thermal_temperature.split("\n")

        for i in range(len(temperature_values) - 1):
            final_temperature = f'{final_temperature}{temperature_values[i]};{thermal_temperature[i]}\n'

    return final_temperature
