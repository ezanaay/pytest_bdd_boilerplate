import logging, sys
from logging.handlers import TimedRotatingFileHandler

import os

from config.project import PROJECT

format_pattern = '%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s'
FORMATTER = logging.Formatter(fmt=format_pattern, datefmt='%Y-%m-%d %H:%M:%S')


def get_log_file_path():
    curr_dir = os.path.abspath(os.path.dirname(__file__))
    log_dir = os.path.join(curr_dir, '..', f'logs/{PROJECT["project_name"]}')
    if not os.path.exists(log_dir): os.makedirs(log_dir)
    return f"{log_dir}/logs.log"


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(format_pattern)
    console_handler.setFormatter(formatter)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(get_log_file_path(), when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name, level='INFO', console_out=False):
    log_level = eval(f"logging.{level}")

    logger = logging.getLogger(logger_name)

    logger.setLevel(log_level)

    if console_out: logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())

    logger.propagate = False

    return logger
