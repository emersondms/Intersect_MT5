import logging
import sys
from datetime import datetime

logs = logging.getLogger()
logs.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

# print the logs 
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
stdout_handler.setFormatter(formatter)

# write logs to a file
file_handler = logging.FileHandler('logs\\{:%Y-%m-%d}.log'.format(datetime.now()))
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logs.addHandler(file_handler)
logs.addHandler(stdout_handler)
