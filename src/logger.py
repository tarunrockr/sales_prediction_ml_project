import logging
import os
from datetime import datetime, date

today_date = datetime.today().strftime("%d_%m_%Y")
log_folder_path = os.path.join(os.getcwd(), 'logs', today_date)
os.makedirs(log_folder_path, exist_ok = True)

time = datetime.now().strftime("%d_%m_%Y_%H%M%S")
log_filename =  'log_'+time+".log"
log_filepath = os.path.join(log_folder_path, log_filename)

# Setting logging level, filename and format
# '%(name)s' is 'root'
# '%(asctime)s' for time
# '%(lineno)d' line no where we are adding log information
# '%(levelname)s' such as [INFO, DEBUG, WARNING, ERROR, CRITICAL]
# '%(message)s' for logging data
logging.basicConfig(filename= log_filepath, level= logging.INFO, format= "[%(asctime)s] %(lineno)d %(name)s  - %(levelname)s:%(message)s")


# if __name__ == "__main__":
#     logging.info("Test data for logging")