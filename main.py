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


def quartlyExport(start_q, end_q):
    for i in range(start_q, end_q+1):
        fromdate1, today1 = get_specific_fiscal_quarter_date(i)
        main_tally.tally_prime_api_export_data(company=list(kb_daily_exported_data.keys()),fromdate=fromdate1, todate=today1,extra_reports=True)
        main_db.delete_tally_data_file_wise(start_date=fromdate1,end_date=today1, file_date=today1, commit=True)
        main_db.import_tally_data(date=today1)
        logger.info(f"Completed This Quarter from {fromdate1} and to date is {today1} and quarter is {i}")




def item_mapping_import(file_path: Optional[str], outstanding: Optional[bool] = False, item_master: Optional[bool] = False) -> dict:
    try:
        if not file_path:
            raise ValueError("File path not provided.")

        enabled_flags = []
        if item_master:
            enabled_flags.append("item_master")
        if outstanding:
            enabled_flags.append("outstanding")

        logger.info(f"Enabled modes: {', '.join(enabled_flags) if enabled_flags else 'None'}")

        KBEBase.metadata.create_all(bind=kbe_engine)

        df = pd.read_excel(file_path)
        df.columns = df.columns.str.lower().str.replace(" ", "_")

        db_crud = DatabaseCrud(db_connector=kbe_engine)

        if item_master == True:
            df['fcy'] = np.where(df['material_centre'].isin(fcy_comp), 'Yes', 'No')

            required_cols = ['item_name', 'item_alias', 'parent', 'unit',
                             'material_centre', 'fcy', 'mapping', 'conversion', 'alt_unit']
            missing = [col for col in required_cols if col not in df.columns]
            if missing:
                raise ValueError(f"Missing required column(s): {', '.join(missing)}")

            validation_mc = [
                'FCY Frexotic', 'FCY KBE', 'FCY KBEIPL', 'FCY Orbit', 'FCY KBAIPL',
                'FCY Freshnova', 'Vashi KBEIPL', 'Vashi KBE', 'Thane KBE', 'USA KB Fruits',
                'Thane Indifruit', 'Thane Perfect Produce', 'Thane KB Fresh', 'Thane Freshnova', 'Thane Aamrica',
                'Thane KBAFPL', 'MP KBVPL', 'MP KBFV&FPL', 'MP F&VPL', 'MP KBFMSPL',
                'MP KBAIPL', 'Thane KBEIPL', 'Thane Fab Fresh', 'Nagar KBEIPL', 'Gujarat KBEIPL',
                'Cargo KBEIPL', 'Nagar NA KBE', 'Nagar A KBE', 'Gujarat KBE', 'MP KBE',
                'JDS KBE', 'Cargo KBE', 'Thane Orbit', 'Gujarat Orbit', 'Thane Frexotic',
                'Gujarat KBAIPL', 'Thane KBAIPL', 'UK KB Veg',"Phaltan NA KBE"]
            invalid_mc = set(df['material_centre'].dropna()) - set(validation_mc)
            if invalid_mc:
                raise ValueError(f"Invalid material_centre(s): {invalid_mc}")

            for col in [c for c in required_cols if c != 'conversion']:
                df[col] = df[col].apply(api_utils.clean_string)

            df = df.applymap(lambda x: x.replace("_x000D_", "").strip("\r\n") if isinstance(x, str) else x)

            df['conversion'] = pd.to_numeric(df['conversion'], errors='coerce')

            db_crud.import_data(table_name='tally_item_mapping', df=df, commit=True)
            logger.info(f"{len(df)} new rows imported into tally_item_mapping.")
            return {"imported": df.to_dict(orient="records"), "skipped": []}

        if outstanding:
            required_cols = ["particulars", "material_centre", "credit_period", "country", "responsible"]
            missing = [col for col in required_cols if col not in df.columns]
            if missing:
                raise ValueError(f"Missing required column(s): {', '.join(missing)}")

            df['credit_period'] = df['credit_period'].fillna(0)
            df['responsible'] = df['responsible'].astype(str).str.title()

            db_crud.import_data(table_name='tally_outstanding_mapping', df=df, commit=True)
            logger.info(f"{len(df)} new rows imported into tally_outstanding_mapping.")
            return {"imported": df.to_dict(orient="records"), "skipped": []}

    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
    except ValueError as ve:
        logger.error(f"Validation Error: {ve}")
    except SQLAlchemyError as se:
        logger.error(f"Database Error: {se}")
    except Exception as e:
        logger.exception(f"Unexpected Error: {e}")

    return {"imported": [], "skipped": []}



if __name__ == "__main__": 
    quartlyExport(1,2)







    

    
    









    









