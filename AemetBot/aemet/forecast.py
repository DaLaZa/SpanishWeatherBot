from datetime import datetime
from .constants import *


# Checks the dates to return the correct one
def check_result_dates(result, date_time):
    date_today_format = "%Y-%m-%d %H:%M:%S.%f"
    date_today = str(datetime.strptime(str(date_time), date_today_format).strftime("%d-%b-%Y"))

    for value in range(4):
        date_result = result[0]["prediccion"]["dia"][value]["fecha"]
        date_json = str(datetime.strptime(date_result, DATA_TYPE).strftime("%d-%b-%Y"))

        if date_today == date_json:
            return value
    return 0


# Get the last load values and golden hours
def golden_hours(scheduled_result, correct_value_date):
    sunrise = scheduled_result[0]["prediccion"]["dia"][correct_value_date]["orto"]
    sunset = scheduled_result[0]["prediccion"]["dia"][correct_value_date]["ocaso"]
    elaboration = scheduled_result[0]["elaborado"]
    date = str(datetime.strptime(elaboration, DATA_TYPE).strftime("%d-%b-%Y; %H:%M:%S"))

    return f'ULTIMA ACTUALIZACION: {date}\nAMANECE:  {sunrise}\nANOCHECE: {sunset}\n\n'


# Get the sky condition
def sky_condition_scheduled(scheduled_result, correct_value_date, current_hour, hour=None):
    ranges = {element["periodo"]: element["descripcion"] for element in
              scheduled_result[0]["prediccion"]["dia"][correct_value_date]["estadoCielo"]}

    sky_condition = SKY_CONDITION

    if hour is None:
        for key, value in ranges.items():
            if int(key) >= current_hour:
                sky_condition = f'{sky_condition}{key}h: {value}\n'
    else:
        for key, value in ranges.items():
            if hour < int(key):
                raise ValueError
            elif hour == int(key):
                sky_condition = f'{sky_condition}{key}h: {value}\n\n'
                break

    return sky_condition


# Get the probability of precipitation
def probability_precipitation_scheduled(scheduled_result, correct_value_date, current_hour, hour=None):
    ranges = {element["periodo"]: element["value"] for element in
              scheduled_result[0]["prediccion"]["dia"][correct_value_date]["probPrecipitacion"]}

    precipitation = PRECIPITATION_PROBABILITY
    check_hour = False

    if hour is None:
        for key, value in ranges.items():
            if current_hour <= int(key[0:2]):
                check_hour = True
                precipitation = f'{precipitation}Entre las: {key[0:2]}h-{key[2:4]}h: {str(value)}%\n'
            if int(key[2:4]) == 1 and check_hour is False:
                if current_hour <= 24:
                    precipitation = f'{precipitation}Entre las: {key[0:2]}h-{key[2:4]}h: {str(value)}%\n'
    else:
        for key, value in ranges.items():
            if int(key[2:4]) < int(key[0:2]):
                real_hour = 24
            else:
                real_hour = int(key[2:4])
            if hour in range(int(key[0:2]), real_hour):
                precipitation = f'{precipitation}Entre las: {key[0:2]}h-{key[2:4]}h: {str(value)}%\n\n'
                break

    return precipitation


# Get the precipitation hours
def precipitation_scheduled(scheduled_result, correct_value_date, current_hour, hour=None):
    ranges = {element["periodo"]: element["value"] for element in
              scheduled_result[0]["prediccion"]["dia"][correct_value_date]["precipitacion"]}

    precipitation = PRECIPITATION

    if hour is None:
        for key, value in ranges.items():
            if int(key) >= current_hour:
                precipitation += f'{key}h: {value} (mm)\n'
    else:
        for key, value in ranges.items():
            if hour < int(key):
                return ""
            elif hour == int(key):
                precipitation += f'{key}h: {value} (mm)\n\n'
                break

    return precipitation


# Get the probability of snowing
def probability_snow_scheduled(scheduled_result, correct_value_date, current_hour, hour=None):
    ranges = {element["periodo"]: element["value"] for element in
              scheduled_result[0]["prediccion"]["dia"][correct_value_date]["probNieve"]}

    snow = SNOW_PROBABILITY
    check_hour = False

    if hour is None:
        for key, value in ranges.items():
            if current_hour <= int(key[0:2]):
                check_hour = True
                snow = f'{snow}Entre las: {key[0:2]}h-{key[2:4]}h: {str(value)}%\n'
            if int(key[2:4]) == 1 and check_hour is False:
                if current_hour <= 24:
                    snow = f'{snow}Entre las: {key[0:2]}h-{key[2:4]}h: {str(value)}%\n'
    else:
        for key, value in ranges.items():
            if int(key[2:4]) < int(key[0:2]):
                real_hour = 24
            else:
                real_hour = int(key[2:4])
            if hour in range(int(key[0:2]), real_hour):
                snow = f'{snow}Entre las: {key[0:2]}h-{key[2:4]}h: {str(value)}%\n\n'
                break

    return snow


# Get the snow precipitation
def snow_scheduled(scheduled_result, correct_value_date, current_hour, hour=None):
    ranges = {element["periodo"]: element["value"] for element in
              scheduled_result[0]["prediccion"]["dia"][correct_value_date]["nieve"]}

    snow = SNOW

    if hour is None:
        for key, value in ranges.items():
            if int(key) >= current_hour:
                snow = f'{snow}{key}h: {value} (mm)\n'
    else:
        for key, value in ranges.items():
            if hour == int(key):
                snow = f'{snow}{key}h: {value} (mm)\n\n'
                break

    return snow


# Get the temperature and thermal sensation
def temperature_scheduled(scheduled_result, correct_value_date, current_hour, hour=None):
    current_temperature = {element["periodo"]: element["value"] for element in
                           scheduled_result[0]["prediccion"]["dia"][correct_value_date]["temperatura"]}

    thermal_sensation = {element["periodo"]: element["value"] for element in
                         scheduled_result[0]["prediccion"]["dia"][correct_value_date]["sensTermica"]}

    temperature_values = ""
    thermal_temperature = ""
    final_temperature = TEMPERATURE

    if hour is None:
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

    else:
        for key_temperature, value_temperature in current_temperature.items():
            if hour == int(key_temperature):
                final_temperature = f'{final_temperature}{key_temperature}h: Temperatura: {value_temperature}ºC;'
                break

        for key, value in thermal_sensation.items():
            if hour == int(key):
                final_temperature = f'{final_temperature} Sensacion termica: {value}ºC\n\n'
                break

    return final_temperature
