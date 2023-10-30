# -*- coding: utf-8 -*-

import os
import logging
import colorlog
import time

logger = logging.getLogger('ToolLog')
log_path = 'logs'

def log(loglevel, log_name):
    if os.path.isdir(log_path) is not True:
        os.mkdir(log_path, 0o755)

    logfile = os.path.join(log_path, log_name + '.log')

    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            fmt='%(log_color)s[%(levelname)s] [%(threadName)s] [%(asctime)s] [%(filename)s:%(lineno)d] %(message)s',
            datefmt="%H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
        )
    )
    f = open(logfile, 'a+')
    handler2 = logging.StreamHandler(f)
    formatter = logging.Formatter(
        "[%(levelname)s] [%(threadName)s] [%(asctime)s] [%(filename)s:%(lineno)d] %(message)s")
    handler2.setFormatter(formatter)
    logger.addHandler(handler2)
    logger.addHandler(handler)

    logger.setLevel(logging.INFO)


class DLogger:
    def __init__(self, logger, logger2):
        self.logger = logger
        self.logger2 = logger2

    def info(self, message):
        self.logger.info(message)
        self.logger2.info(message)

    def debug(self, message):
        self.logger.debug(message)
        self.logger2.debug(message)

    def warn(self, message):
        self.logger.warn(message)
        self.logger2.warn(message)

    def warning(self, message):
        self.logger.warn(message)
        self.logger2.warn(message)

    def error(self, message):
        self.logger.error(message)
        self.logger2.error(message)

    def critical(self, message):
        self.logger.critical(message)
        self.logger2.critical(message)

