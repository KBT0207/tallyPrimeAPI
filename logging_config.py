import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime

# Custom UTF-8 encoded TimedRotatingFileHandler
class TimedRotatingFileHandlerUtf8(TimedRotatingFileHandler):
    def __init__(self, filename, when='midnight', interval=1, backupCount=7, encoding='utf-8', **kwargs):
        super().__init__(filename, when=when, interval=interval, backupCount=backupCount, encoding=encoding, **kwargs)

# Register the custom handler class so logging can use it by name
logging.handlers.TimedRotatingFileHandlerUtf8 = TimedRotatingFileHandlerUtf8

today_date = datetime.now().strftime('%d-%b-%Y')
log_directory = 'E:/logs'
log_file = os.path.join(log_directory, f"main_{today_date}.log")

os.makedirs(log_directory, exist_ok=True)

LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s'
        }
    },
    'handlers': {
        'console_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': 'INFO'
        },
        'file_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandlerUtf8',  # use custom UTF-8-safe handler
            'filename': log_file,
            'when': 'midnight',
            'interval': 1,
            'backupCount': 30,
            'formatter': 'standard',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console_handler', 'file_handler'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("main")
