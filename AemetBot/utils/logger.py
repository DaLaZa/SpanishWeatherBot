from datetime import datetime
import logging

# Create log application
date_time = datetime.today()
date_today_format = "%Y-%m-%d %H:%M:%S.%f"
date_today = str(datetime.strptime(str(date_time), date_today_format).strftime("%Y%m%d"))
log_file = f'log/application_log_{date_today}'
logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s; %(message)s", filemode="a+")

logger = logging.getLogger()
