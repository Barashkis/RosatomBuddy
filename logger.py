import logging
import datetime
import os

from config import logs_dir, timezone


class Formatter(logging.Formatter):
    @staticmethod
    def converter(timestamp):
        dt = datetime.datetime.fromtimestamp(timestamp)

        return dt

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created).astimezone(timezone)

        if datefmt:
            s = dt.strftime(datefmt)
        else:
            try:
                s = dt.isoformat(timespec='milliseconds')
            except TypeError:
                s = dt.isoformat()

        return s


if not os.path.exists("logs"):
    os.mkdir("logs")

today = datetime.datetime.today().astimezone(timezone)
filename = f'{today.day:02d}-{today.month:02d}-{today.year}.log'

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(os.path.join(logs_dir, filename))
file_handler.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

formatter = Formatter('%(asctime)s: %(filename)s: %(levelname)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
