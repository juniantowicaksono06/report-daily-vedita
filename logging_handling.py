import os
from datetime import datetime
from utils import prepend_zero
import logging
import traceback

def error_logging(message = None):
    date = datetime.now()
    year = date.year
    month = prepend_zero(date.month)
    day = prepend_zero(date.day)
    logs_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs')
    logs_folder = os.path.join(logs_folder, 'error')
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)
    logs_file = os.path.join(logs_folder, "error_{}_{}_{}.txt".format(year, month, day))
    logger = logging.getLogger(__name__)

    # Set the logging level to ERROR or higher
    logger.setLevel(logging.ERROR)
    file_handler = logging.FileHandler(logs_file)
    file_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    if message is None:
        tb = traceback.format_exc()
    else:
        tb = message
    logger.error('An error occurred: %s', tb)

def info_logging(message: str = None):
    date = datetime.now()
    year = date.year
    month = prepend_zero(date.month)
    day = prepend_zero(date.day)
    logs_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs')
    logs_folder = os.path.join(logs_folder, 'info')
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)
    logs_file = os.path.join(logs_folder, "info_{}_{}_{}.txt".format(year, month, day))
    logger = logging.getLogger(__name__)

    # Set the logging level to ERROR or higher
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(logs_file)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.info('LOG: %s', message)