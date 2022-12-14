import logging
import datetime

from config import timezone


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


filename = f"logfile.log"

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(filename)
file_handler.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

formatter = Formatter('%(asctime)s: %(filename)s: %(levelname)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
