import sys
import time
from datetime import date, datetime, timedelta
import pandas as pd
from database import main_db, tally_data_processor
from database.db_crud import DatabaseCrud
from logging_config import logger
from tally import main_tally, tally_utils,api_utils
from utils.common_utils import (kb, get_specific_fiscal_quarter_date, demo_export)
from database.sql_connector import kbe_engine
from database.models.base import KBEBase
import glob
import os
from xlwings import view


def quartlyExport(start_q, end_q):
    for i in range(start_q, end_q+1):
        fromdate1, today1 = get_specific_fiscal_quarter_date(i)
        main_tally.tally_prime_api_export_data(company=list(kb.keys()),fromdate=fromdate1, todate=today1)
        main_db.delete_tally_data_file_wise(start_date=fromdate1,end_date=today1, file_date=today1, commit=True)
        main_db.import_tally_data(date=today1)
        logger.info(f"Completed This Quarter from {fromdate1} and to date is {today1}")



if __name__ == "__main__": 
    
    # quartlyExport(13,20)
    quartlyExport(1,2)








    









