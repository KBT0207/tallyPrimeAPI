import logging
import logging.config
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from utils.email import  YagmailHandler
import yagmail
import os
from datetime import datetime
from logtail import LogtailHandler



yag = yagmail.SMTP('vivekkumar@kaybeeexports.com', os.getenv('SENDER_EMAIL_PASSWORD'))

email_recipients = ['s.gaurav@kaybeeexports.com', 'danish@kaybeeexports.com']
#email_recipients = ['s.gaurav@kaybeeexports.com']


today_date = datetime.now().strftime('%d-%b-%Y').replace(':', '-')

log_directory = 'E:/logs'
log_file = os.path.join(log_directory, f"main_{today_date}.log")
if not os.path.exists(log_directory):
    os.makedirs(log_directory)


# Logging configuration
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
        },
        'critical_email_handler': {
            'class': 'logging.handlers.MemoryHandler',
            'target': 'yagmail_handler',
            'level': 'CRITICAL',
            'formatter': 'standard',
            'capacity': 100
        },
        'yagmail_handler': {
            'class': 'utils.email.YagmailHandler',
            'to': email_recipients,
            'subject': 'Critical Log',
            'formatter': 'standard'
        },
        'better_stack_handler':{
            'class': 'logtail.LogtailHandler',
            'formatter': 'standard',
            'level': 'INFO',
            'source_token': os.getenv('SOURCE_TOKEN')
        }

    },
    'loggers': {
        '': {
            'handlers': [
                        'console_handler',
                        'file_handler', 
                        # 'critical_email_handler', 
                        'better_stack_handler',
                        ],
            'level': 'INFO',
            'propagate': False
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger("main")

