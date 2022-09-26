"""
@Time ： 2022/4/13 10:43
@Auth ： Ted
@File ：LogConfig.py
@IDE ：PyCharm
"""


CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'format': '{asctime} {filename:s} {module} {funcName:s} {levelname} {message}',
            'style': '{',
        },
        'detail': {
            'format': '{asctime} {process:d} {thread:d} {pathname:s} {module} {funcName:s} {levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        # 'file': {
        #     'level': 'INFO',
        #     # 'class': 'logging.FileHandler',
        #     'class': 'logging.handlers.TimedRotatingFileHandler',  # 改为日志滚动
        #     'formatter': 'default',
        #     'filename': os.path.join(LOG_PATH, LOG_FILE_NAME),
        #     'when': 'H',
        #     'interval': 6,
        #     'backupCount': 100,
        #     'encoding': 'utf-8',
        # },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'default',
        },
    },
    'loggers': {
        'default': {
            'handlers': ['console'],
            'level': 'INFO',
            'formatter': 'default',
            'propagate': True,
        },
    },
}
