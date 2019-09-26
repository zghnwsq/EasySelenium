# coding=utf-8

import sys
import logging


def logger(log_level):
    formatter = logging.Formatter(' %(asctime)s - %(levelname)s: %(message)s',
                                  datefmt='%Y-%m-%d %A %H:%M:%S')
    logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    lev = getattr(logging, log_level.upper())
    logger.setLevel(lev)
    return logger
