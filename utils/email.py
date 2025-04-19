import logging
import os
import schedule
from datetime import datetime, time
from dotenv import load_dotenv
import yagmail


load_dotenv(".env")


yag = yagmail.SMTP("vivekkumar@kaybeeexports.com", 
                   os.getenv('SENDER_EMAIL_PASSWORD')) 
# Adding Content and sending it 


def email_send(reciever, cc = None, bcc = None, subject=None, contents= None, attachemnts=None):
    yag.send(to= reciever, 
             cc= cc ,
             bcc= bcc, 
             subject = subject, 
             contents= contents, 
             attachments= attachemnts)

                

class YagmailHandler(logging.Handler):
    def __init__(self, to, subject, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.to = to
        self.subject = subject

    def emit(self, record):
        log_entry = self.format(record)
        yag.send(to=self.to, subject=self.subject, contents=log_entry)


today_date = datetime.now().strftime('%d-%b-%Y')
email_recipients = ['s.gaurav@kaybeeexports.com', 
                    'danish@kaybeeexports.com',
]


def send_daily_logs():
    # Read the contents of the log file
    log_file_path = f'logs/main_{today_date}.log'
    with open(log_file_path, 'r') as log_file:
        log_contents = log_file.read()

    # Send the log contents via Yagmail
    yag.send(to=email_recipients, subject=f'Daily Log of {today_date}', contents=log_contents)


