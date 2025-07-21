import pandas as pd
from xlwings import view
import numpy as np
from logging_config import logger
from io import BytesIO
from xlwings import view
import os
import io
import time
import re
import json
from datetime import datetime
import numpy as np
from tally.api_utils  import fcy_comp, symbol_to_currency, json_data_convert_amount_in_string, curr
import warnings


def APISalesReturnVoucher(file_path: str, material_centre_name: str):
    try:
        data = json_data_convert_amount_in_string(file_path)
        raw_data = data['ENVELOPE']['Body']
    except Exception as e:
        print(f"json convert error {e}")
        return pd.DataFrame()

    try:
        for voucher in raw_data:
            voucher.setdefault('BillDetails', [])
    except Exception as e:
        print(f"Error processing vouchers: {e}")
        return pd.DataFrame()

    if not raw_data:
        print("No data found in 'Body'")
        return pd.DataFrame()

    sample_voucher = raw_data[0]
    meta_cols = [key for key in sample_voucher.keys() if key != 'BillDetails']

    df = pd.json_normalize(raw_data, record_path='BillDetails', meta=meta_cols, errors='ignore',meta_prefix="_meta")
    df = df.applymap(lambda x: x.replace('\r\n', '').replace('\\u0004', '') if isinstance(x, str) else x)
    df.columns = df.columns.str.lower().str.replace(" ","_")
    cols = {
        'bill_date':"date",
        'bill_name':"voucher_no",
        '_metaledger_name':"customer_name"
    }
    df.rename(columns=cols,inplace=True)
    df = df.dropna(subset=["due_amount"])

    df['date'] = pd.to_datetime(df['date'], format='%d-%b-%y', errors='coerce')
    df['currency'] = df['due_amount'].astype(str).str.extract(r'(AU\$|A\$|CAD|£|€|\$)')
    df['currency'] = df['currency'].map(symbol_to_currency)
    df['currency'] = df['currency'].fillna("Unknown")

    df['_metarate_of_exchange'] = df['_metarate_of_exchange'].str.replace("₹", "", regex=False)
    df['extracted_symbol'] = df['_metarate_of_exchange'].astype(str).str.extract(r'(AU\$|A\$|CAD|£|€|\$)', expand=False)
    df['mapped_currency'] = df['extracted_symbol'].map(symbol_to_currency)
    df.loc[(df['currency'] == 'Unknown') & (df['mapped_currency'].notnull()), 'currency'] = df['mapped_currency']
    df.drop(columns=['extracted_symbol', 'mapped_currency'], inplace=True)
    df['due_amount'] = df['due_amount'].replace(r'[^\d.]', '', regex=True)
    df['due_amount'] = pd.to_numeric(df['due_amount'], errors='coerce').fillna(0)


    df['currency'] = np.where(
        (df['currency'] == 'Unknown') & (df['_metaledger_group'].str[:3] == 'INR'),
        'INR',
        df['currency']
    )

    df['material_centre'] = material_centre_name
    df['fcy'] = np.where(df['material_centre'].isin(fcy_comp), 'Yes', 'No')
    final_col = ['date','voucher_no','customer_name','due_amount','currency','material_centre','fcy']
    df = df[final_col]



    return df

import datetime

def get_quarter_month_range(date):
    month = date.month
    if 4 <= month <= 6:
        return (4, 6)
    elif 7 <= month <= 9:
        return (7, 9)
    elif 10 <= month <= 12:
        return (10, 12)
    else:
        return (1, 3)
    
if __name__ == "__main__":
    date = datetime.date(2025, 7, 21)
    start_month, end_month = get_quarter_month_range(date)
    print(f"Start Month: {start_month}, End Month: {end_month}")

