# coding=utf-8

import sys
import logging


def logger(log_level):
    """
    标准输出日志对象
    :param log_level: 日志级别
    :return:日志对象
    """
    formatter = logging.Formatter(' %(asctime)s - %(levelname)s: %(message)s',
                                  datefmt='%Y-%m-%d %A %H:%M:%S')
    log = logging.getLogger()
    if not log.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        log.addHandler(handler)
    lev = getattr(logging, log_level.upper())
    log.setLevel(lev)
    return log
