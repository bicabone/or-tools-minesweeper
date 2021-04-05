import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from dotenv import load_dotenv
import os


class Config:
    """
    Make .env variables available throughout the application by importing from this module
    """

    def __init__(self) -> None:
        super().__init__()
        load_dotenv()
        self.environ = os.environ

    def get(self, key, default=None):
        if default:
            return self.environ.get(key, default)
        else:
            return self.environ.get(key)


config = Config()

"""
Configure logging formatter and rotating file handler
"""
logging.root.setLevel(logging.NOTSET)

log_folder_location = config.get(
    "LOG_LOCATION",
    f"{Path(__file__).parents[1]}/log"
)
if not os.path.exists(log_folder_location):
    os.makedirs(log_folder_location)

log_file_location = f'{log_folder_location}/application.log'

# 500 kilobytes
max_bytes = 1000 * 500
rotating_handler = RotatingFileHandler(
    log_file_location,
    mode='a',
    maxBytes=max_bytes,
    backupCount=10
)
formatter = logging.Formatter(
    "%(asctime)s %(levelname)s [%(threadName)s]"
    " %(module)s.%(funcName)s:%(lineno)d"
    " : %(message)s"
)

"""
Initialize logger for this module
"""
log = logging.getLogger(__name__)
if config.get("ENVIRONMENT", "LOCAL") == "LOCAL":
    log.setLevel(logging.DEBUG)
else:
    log.setLevel(logging.INFO)

rotating_handler.setFormatter(formatter)
log.addHandler(rotating_handler)

"""
Set stream handler to get console logs
"""
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
log.addHandler(stream_handler)
