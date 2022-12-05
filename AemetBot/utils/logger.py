from AemetBot import _ROOT_DIR
from datetime import datetime
import logging
import os

# Create log application
date_time = datetime.today()
date_today_format = "%Y-%m-%d %H:%M:%S.%f"
date_today = str(datetime.strptime(str(date_time), date_today_format).strftime("%Y%m%d"))

# Chek if log dir exists if not create it
isExist = os.path.exists(os.path.join(_ROOT_DIR, "log"))
if not isExist:
    os.makedirs(os.path.join(_ROOT_DIR, "log"))

log_file = f'{_ROOT_DIR}/log/application_log_{date_today}'
logging.basicConfig(filename=log_file, level=logging.ERROR, format="%(asctime)s; %(message)s", filemode="a+")

logger = logging.getLogger()
