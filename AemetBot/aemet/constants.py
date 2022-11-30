import json
import os.path

from AemetBot import _ASSETS_PATH


BASE_URL = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones/"
API_URL = "https://opendata.aemet.es/opendata/api"
MUNICIPALITY_URL = API_URL + "/maestro/municipios"
SCHEDULED_PREDICTION = API_URL + "/prediccion/especifica/municipio/horaria/{codigo}"
DAILY_PROVINCIAL_PREDICTION_DATE = API_URL + "/prediccion/provincia/hoy/{province}/elaboracion/{date}"
DAILY_PROVINCIAL_PREDICTION = API_URL + "/prediccion/provincia/hoy/{province}"
COMMUNITY_PREDICTION = API_URL + "/prediccion/ccaa/manana/{community}"
DATA_STATION = API_URL + "/observacion/convencional/datos/estacion/8368U"
TEMPERATURES = "TEMPERATURAS"
DATA_BASE_NAME = os.path.join(_ASSETS_PATH, "community_codes.db")
MUNICIPALITY_FILE = os.path.join(_ASSETS_PATH, "municipalityCodes.xls")
PRECIPITATION = "\nLLUVIA\n"
SKY_CONDITION = "ESTADO DEL CIELO\n"
PRECIPITATION_PROBABILITY = "\nPROBABILIDAD DE LLUVIA\n"
SNOW_PROBABILITY = "\nPROBABILIDAD DE NIEVE\n"
SNOW = "\nNIEVE ACUMULADA\n"
TEMPERATURE = "\nTEMPERATURA\n"
DATA_TYPE = "%Y-%m-%dT%H:%M:%S"
VALUE_ERROR = "No se han encontrado datos."
DATA_ERROR_MESSAGE = "Error retrieving data of"
API_ERROR = "Error con la conexión, probar más tarde"
NO_DATA_HOUR = "No existe predicción para esa hora."
PROVINCE = "PROVINCIA DE "

with open(os.path.join(_ASSETS_PATH, "credentials.json"), "r") as f:
    AEMET_API_KEY = json.load(f)["AEMET_API_KEY"]
