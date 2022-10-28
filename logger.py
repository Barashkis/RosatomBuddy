import logging
import datetime as dt
import os

from config import logs_dir, timezone

if not os.path.exists("logs"):
    os.mkdir("logs")

today = dt.datetime.today().astimezone(timezone)
filename = f'{today.day:02d}-{today.month:02d}-{today.year}.log'

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(os.path.join(logs_dir, filename))
file_handler.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s: %(filename)s: %(levelname)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
