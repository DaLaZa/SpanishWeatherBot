import json
import os.path
from AemetBot import _ASSETS_PATH, _ROOT_DIR

LAST_UPDATE_PATH = os.path.join(_ROOT_DIR, "telegram_bot", "last_update.txt")
START_MESSAGE = "Esto es un bot para ver la predicción del tiempo en España. La información se obtiene de la API de " \
                "AEMET y muestra la previsión del día actual. Para saber como funciona, utilice el comando de ayuda " \
                "/help"
HELP_MESSAGE = "Para conocer el tiempo de una ciudad o municipio, debe escribir el nombre " \
               "de este y enviarlo.\nEjemplo: Teruel \nSi además quiere saber una hora exacta debe mandar el nombre " \
               "de la ciudad/municipio seguido de punto y coma ';' y la hora.\nEjemplo: Teruel; 14\n. Si desea conocer"\
               " la previsión para un rango de horas concreto, debe de escribir el nombre de la ciudad/municipio, " \
               "seguido de punto y coma ';' después la primera hora, un guión '-' y la segunda hora." \
               "\nEjemplo: Teruel; 21-23\nImportante, el rango de horas va desde las 00 hasta las 23.\nTambién puede " \
               "revisar la previsión del día siguiente utilizando el comando '/m'\nEjemplo: /m Teruel; 14 "
ERROR_MUNICIPALITY = "Formato incorrecto. Se debe mandar una ciudad/municipio, seguido de punto y coma ';' y la " \
                     "hora.\nEjemplo: Teruel; 14 "
ERROR_NUMERIC = "Hora incorrecta"
MUNICIPALITY_NAME_ERROR = "Problem with municipality name"
HOUR_PROBLEM = "Rango de horas incorrecto"
NO_DATA_HOUR = "No existe predicción para esa hora."

with open(os.path.join(_ASSETS_PATH, "credentials.json"), "r") as f:
    TOKEN = json.load(f)['TELEGRAM_BOT_KEY']
