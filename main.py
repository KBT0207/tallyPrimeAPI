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
from tally.api_utils  import fcy_comp, symbol_to_currency, json_data_convert_amount_in_string, curr, extract_all_postal_codes, clean_string
import numpy as np


def quartlyExport(start_q, end_q):
    for i in range(start_q, end_q+1):
        fromdate1, today1 = get_specific_fiscal_quarter_date(i)
        main_tally.tally_prime_api_export_data(company=list(kb_daily_exported_data.keys()),fromdate=fromdate1, todate=today1,extra_reports=True)
        main_db.delete_tally_data_file_wise(start_date=fromdate1,end_date=today1, file_date=today1, commit=True)
        main_db.import_tally_data(date=today1)
        logger.info(f"Completed This Quarter from {fromdate1} and to date is {today1} and quarter is {i}")



def item_mapping_import(file_path: Optional[str]) -> dict:
    try:
        if not file_path:
            raise ValueError("File path not provided.")

        logger.info("Starting item mapping import")

        KBEBase.metadata.create_all(bind=kbe_engine)

        # Load and normalize column names
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.lower().str.replace(" ", "_")

        # Required columns
        all_cols = ['item_name', 'item_alias', 'parent', 'unit',
                    'material_centre', 'fcy', 'mapping', 'conversion', 'alt_unit']
        for col in all_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        # Text columns to clean
        text_cols = [col for col in all_cols if col != 'conversion']

        # Validation list for 'material_centre'
        validation_mc = [
            'FCY Frexotic', 'FCY KBE', 'FCY KBEIPL', 'FCY Orbit', 'FCY KBAIPL',
            'FCY Freshnova', 'Vashi KBEIPL', 'Vashi KBE', 'Thane KBE', 'USA KB Fruits',
            'Thane Indifruit', 'Thane Perfect Produce', 'Thane KB Fresh', 'Thane Freshnova', 'Thane Aamrica',
            'Thane KBAFPL', 'MP KBVPL', 'MP KBFV&FPL', 'MP F&VPL', 'MP KBFMSPL',
            'MP KBAIPL', 'Thane KBEIPL', 'Thane Fab Fresh', 'Nagar KBEIPL', 'Gujarat KBEIPL',
            'Cargo KBEIPL', 'Nagar NA KBE', 'Nagar A KBE', 'Gujarat KBE', 'MP KBE',
            'JDS KBE', 'Cargo KBE', 'Thane Orbit', 'Gujarat Orbit', 'Thane Frexotic',
            'Gujarat KBAIPL', 'Thane KBAIPL', 'UK KB Veg',
        ]

        # Check for invalid material centres
        invalid_mc = set(df['material_centre'].dropna().unique()) - set(validation_mc)
        if invalid_mc:
            raise ValueError(f"Invalid material_centre(s): {invalid_mc}")

        # Clean text columns
        for col in text_cols:
            df[col] = df[col].apply(api_utils.clean_string)

        # Remove special line breaks
        df = df.applymap(lambda x: x.replace("_x000D_", "") if isinstance(x, str) else x)
        df = df.applymap(lambda x: x.strip("\r\n") if isinstance(x, str) else x)


        # Ensure 'conversion' is numeric
        if 'conversion' in df.columns:
            df['conversion'] = pd.to_numeric(df['conversion'], errors='coerce')

        # Import into DB
        db_crud = DatabaseCrud(db_connector=kbe_engine)
        db_crud.import_data(table_name='tally_item_mapping', df=df, commit=True)

        logger.info(f"{len(df)} new rows imported.")
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



def testing(file_path: str, material_centre_name: str):
    try:
        data = json_data_convert_amount_in_string(file_path)
        raw_data = data['ENVELOPE']['Body']
    except Exception as e:
        print(f'Error loading data: {e}')
        return pd.DataFrame()

    for voucher in raw_data:
        voucher.setdefault('Ledger', [])
        voucher.setdefault('Bank Details', [])
        for ledger in voucher['Ledger']:
            ledger.setdefault('Bill Allocations', [])

    meta_cols = [col for col in raw_data[0].keys() if col not in ['Ledger', 'Bank Details', 'Bill Allocations']]

    df = pd.json_normalize(
        raw_data,
        record_path='Ledger',
        meta=meta_cols,
        errors='ignore'
    )

    if df.empty:
        print("No data found in JSON.")
        return pd.DataFrame()


    df['Receipt No'] = df.get('Receipt No', '').fillna('Blank')
    df['Rate Of Exchange'] = df.get('Rate Of Exchange', '')
    df['material_centre'] = material_centre_name

    df['Amount'] = df['Amount'].str.replace(r'[^\d.\-]', '', regex=True)
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0).round(2)

    df['Rate Of Exchange'] = df['Rate Of Exchange'].astype(str).str.replace("₹", "")

    df['currency'] = df['Rate Of Exchange'].str.extract(r'(AU\$|A\$|CAD|£|€|\$)')
    df['currency'] = df['currency'].map(symbol_to_currency).fillna("Unknown")
    df['currency'] = df['currency'].str.replace('Unknown', "").replace("", np.nan)

    df['currency'] = np.where(df['currency'].isnull(), df['material_centre'].map(curr), df['currency'])
    df['fcy'] = np.where(df['material_centre'].isin(fcy_comp), 'Yes', 'No')

    df['Rate Of Exchange'] = df['Rate Of Exchange'].str.replace(r'[^\d.\-]', '', regex=True)
    df['Rate Of Exchange'] = pd.to_numeric(df['Rate Of Exchange'], errors='coerce').fillna(0).round(2)

    df['Amount Type'] = df['Amount Type'].map({'Cr': "Credit", 'Dr': "Debit"})

    cols = ['Amount', 'Forex Amount']
    df.loc[df['Amount Type'] == 'Debit', cols] *= -1

    df.columns = df.columns.str.lower().str.replace(" ", "_", regex=False)
    cols_rename = {
        "partyname": "party_name", 'amount':"inr_amount",
        "receipt_date":"date",'receipt_no':"voucher_no"
        }
    df.rename(columns=cols_rename, inplace=True)
    df['date'] = pd.to_datetime(df['date'], format='%d-%b-%y', errors='coerce')
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    
    df['rate_of_exchange'] = np.where(df['currency'].isin(['INR', 'GBP']), 1, 0)
    

    final_cols = [
        'date', 'voucher_no', 'party_name', 'inr_amount',
        'forex_amount', 'rate_of_exchange', 'amount_type',
        'currency', 'fcy', 'material_centre','narration'
    ]
    
    for col in final_cols:
        if col not in df.columns:
            df[col] = ''

    cols = ['voucher_no', 'party_name', 'amount_type', 'currency','material_centre','narration']
    for col in cols:
        if col in df.columns:
            df[col] = df[col].apply(clean_string)

    df['narration'] = df['narration'].str[:500]

    df = df.applymap(
        lambda x: x.replace("x000D", "").replace("\r\n", "") if isinstance(x, str) else x
        )

    df = df[final_cols]
    df = df[df['party_name'].notnull() & (df['party_name'] != '')]

    return df





if __name__ == "__main__": 
    quartlyExport(3,4)

    







    

    
    









    









