import sys
import time
from datetime import date, datetime, timedelta
import pandas as pd
from database import main_db, tally_data_processor
from database.db_crud import DatabaseCrud
from logging_config import logger
from tally import main_tally, tally_utils,api_utils
from utils.common_utils import (get_specific_fiscal_quarter_date, kb_daily_exported_data)
from database.sql_connector import kbe_engine, kbexports_engine
from database.models.base import KBEBase, KBExportBase, KBBIOBase
from database.models.kbe_models.tally_kbe_models import TallyItemsMapping
import glob
import os
from xlwings import view
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from typing import Optional
from tally.api_utils  import fcy_comp
import numpy as np


path = r"E:\api_download\Vashi KBEIPL\Bulk_Purchase Fruits & Vegetables_26_3_2026_11_09_11_.json"
data = tally_data_processor.APIPurchaseVoucher(file_path=path, material_centre_name='Vashi KBEIPL')
view(data)