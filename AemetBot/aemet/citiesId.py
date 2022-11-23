# Imports
import requests
from AemetBot.utils.logger import logger
import pandas as pd
import unicodedata
import string
import rapidfuzz
from .constants import *

querystring = {"api_key": AEMET_API_KEY}
headers = {'cache-control': "no-cache"}


def get_response(url):
    return requests.request("GET", url, headers=headers, params=querystring)


def get_community_code(community, conn):
    cursor = conn.cursor()
    cursor.execute(f'SELECT abbreviation FROM communities WHERE code = {community}')
    return cursor.fetchone()[0]


def get_province_name(province, conn):
    cursor = conn.cursor()
    cursor.execute(f'SELECT province FROM communities WHERE code = {province}')
    return cursor.fetchone()[0]


def get_community_name(province, conn):
    cursor = conn.cursor()
    cursor.execute(f'SELECT community FROM communities WHERE code = {province}')
    return cursor.fetchone()[0]


def get_province_municipality_code(municipality, id_column):
    return get_all_xls_codes(municipality, id_column)


def set_correct_xls_format(row):
    new_column = f'{row.CPRO}{row.CMUN}'
    row["CodeId"] = new_column
    row["NOMBRE"] = order_city_name(row["NOMBRE"])
    return row


def name_data_treatment(municipality):
    # Remove accents for the municipality
    treated_string = ''.join(c for c in unicodedata.normalize('NFD', municipality) if unicodedata.category(c) != 'Mn')
    # Remove all strings punctuations
    treated_string = ''.join(c for c in unicodedata.normalize('NFD', treated_string) if c not in string.punctuation)
    # Remove all initial and end spaces
    treated_string = treated_string.strip()
    # Uppercase the municipality
    treated_string = treated_string.upper()

    return treated_string


def order_city_name(municipality):
    return ' '.join(municipality.split(",")[::-1])


def get_all_xls_codes(municipality):
    try:
        data_frame = pd.read_excel(MUNICIPALITY_FILE, dtype=str)
    except ValueError:
        logger.error("Problem loading municipalityCodes.xls file", exc_info=True)
        return []

    format_municipality = name_data_treatment(municipality)
    # Create new column "CodeId", with the value of "CPRO" and "CMUN" concatenated
    data_frame = data_frame.apply(set_correct_xls_format, axis=1)
    # Rapidfuzz function to compare the format municipality with the format municipality column in the data frame.
    # returns the most accurate name. With [-1] obtains the id of the line
    result = rapidfuzz.process.extractOne(format_municipality, data_frame["NOMBRE"], processor=name_data_treatment)
    if result[1] > 85:
        id_line = result[-1]
        # Iloc to get the info of specific line Example: data_frame.iloc[id_line]
        return data_frame.loc[id_line, "CodeId"], data_frame.loc[id_line, "CPRO"], data_frame.loc[id_line, "NOMBRE"]
    else:
        logger.debug("Rapidfuzz returns a value smaller than 85")
        return []


