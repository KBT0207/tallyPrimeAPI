import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime

today_date = datetime.now().strftime('%d-%b-%Y').replace(':', '-')

current_directory = os.getcwd()

log_directory = os.path.join(current_directory, 'logs')
log_file = os.path.join(log_directory, f"main_{today_date}.log")

if not os.path.exists(log_directory):
    os.makedirs(log_directory)

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
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': log_file,
            'when': 'midnight',
            'interval': 1,
            'backupCount': 30,
            'formatter': 'standard'
        }
    },
    'loggers': {
        '': {
            'handlers': [
                'console_handler',
                'file_handler',
            ],
            'level': 'INFO',
            'propagate': False
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)


