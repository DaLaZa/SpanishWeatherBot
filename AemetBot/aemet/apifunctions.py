# Imports
from datetime import datetime, timedelta

from .citiesId import *
from AemetBot.utils.logger import logger

querystring = {"api_key": AEMET_API_KEY}
headers = {'cache-control': "no-cache"}


# Definition: API call to return the json with the scheduled prediction
# Variables:
#   municipality_cod: Municipality cod.
# Created: DAVID LAHUERTA ZAYAS
def get_scheduled_prediction(municipality_cod):
    url = SCHEDULED_PREDICTION.format(codigo=municipality_cod)
    return get_json_information(url).json()


# Definition: API call to return the text with the daily provincial prediction
# Variables:
#   province: Province code
#   date: Format date to get the API results
# Created: DAVID LAHUERTA ZAYAS
# Modified:
#   David Lahuerta: 13-Dec-2022: Add date
def get_daily_provincial_prediction(province, date):
    if province == "07":
        province = "072"
    elif province == "35":
        province = "353"
    elif province == "38":
        province = "382"

    try:
        url = DAILY_PROVINCIAL_PREDICTION_DATE.format(province=province, date=date)
        response = get_json_information(url).text
    except KeyError:
        url = DAILY_PROVINCIAL_PREDICTION.format(province=province)
        response = get_json_information(url).text

    return response


# Definition: API call to return the text with tomorrow daily provincial prediction
# Variables:
#   province: Province code
# Created: DAVID LAHUERTA ZAYAS
def get_tomorrow_daily_provincial_prediction(province):
    if province == "07":
        province = "072"
    elif province == "35":
        province = "353"
    elif province == "38":
        province = "382"

    try:
        url = TOMORROW_DAILY_PROVINCIAL_PREDICTION.format(province=province)
        response = get_json_information(url).text
    except KeyError:
        url = DAILY_PROVINCIAL_PREDICTION.format(province=province)
        response = get_json_information(url).text

    return response


# Definition: API call to return the text with daily community prediction
# Variables:
#   community: Community code
#   date: Format date to get the API results
# Created: DAVID LAHUERTA ZAYAS
# Modified:
#   David Lahuerta: 13-Dec-2022: Add date
def get_community_prediction(community, date):
    try:
        url = TODAY_COMMUNITY_PREDICTION.format(community=community, date=date)
        response = get_json_information(url).text
    except KeyError:
        url = COMMUNITY_PREDICTION.format(community=community)
        response = get_json_information(url).text

    return response


# Definition: Call to get the API respone
# Variables:
#   url: Aemet API url
# Created: DAVID LAHUERTA ZAYAS
def get_json_information(url):
    response = requests.request("GET", url, headers=headers, params=querystring)
    result = requests.get(response.json()["datos"])
    logger.info(result, exc_info=True)
    return result
