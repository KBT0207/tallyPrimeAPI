import pandas as pd
from xlwings import view
import numpy as np
from logging_config import logger
from io import BytesIO
import os
import io
import time
import re
import json
from datetime import datetime
import numpy as np
from tally.api_utils  import fcy_comp, symbol_to_currency, json_data_convert_amount_in_string, curr, extract_all_postal_codes, clean_string
import warnings
import re




def get_filename_tally(path:str):
    return path.split("\\")[-1].rsplit("_", 2)  [-2]

def get_compname_tally(path:str):
    return path.split("\\")[-1].rsplit("_", 2)[0]


def get_date_tally(path:str):
    return path.split("\\")[-1].split("_")[-1].removesuffix(".xlsx")



pd.set_option('future.no_silent_downcasting', True)



today = datetime.today().strftime('%d-%m-%Y')
warnings.filterwarnings('ignore')

def APISalesVoucher(file_path: str, material_centre_name: str):
    try:
        data = json_data_convert_amount_in_string(file_path)
        raw_data = data['ENVELOPE']['Body']
    except Exception as e:  
        print(f'{e}')
        
    for voucher in raw_data:
        voucher.setdefault('Items', [])
        voucher.setdefault('Ledger', [])

    sample_voucher = raw_data[0]
    meta_cols = [key for key in sample_voucher.keys() if key not in ['Items', 'Ledger']]
    merge_col = ['VOUCHERKEY', 'Voucher Date', 'Voucher Number', 'Voucher Type', 'Party Name']
    
    for key in merge_col:
        if key not in meta_cols:
            meta_cols.append(key)

    df_item = pd.json_normalize(raw_data, errors='ignore', record_path='Items', meta=meta_cols)


    if not df_item.empty:
        df_item['Voucher Number'] = df_item.get('Voucher Number', '').fillna('Blank')
        if 'Sales Ledger' not in df_item.columns:
            df_item['Sales Ledger'] = ''
        if 'Amount' not in df_item.columns:
            df_item['Amount'] = "0"

        ledger_filterd = df_item.copy()

        ledger_filterd['Amount'] = ledger_filterd['Amount'].astype(str).str.replace(r'[^\d.\-]', '', regex=True)
        ledger_filterd['Amount'] = pd.to_numeric(ledger_filterd['Amount'], errors='coerce').fillna(0).round(2)

        ledger_filterd['helper1'] = (
            ledger_filterd['Voucher Date'].astype(str) + 
            ledger_filterd['Voucher Number'].astype(str) + 
            ledger_filterd['Voucher Type'].astype(str) + 
            ledger_filterd['Party Name'].astype(str) + 
            ledger_filterd['Sales Ledger'].astype(str) + 
            ledger_filterd['Amount'].astype(str))

        ledger_group_key = ['Voucher Date', 'Voucher Number', 'Voucher Type', 'Party Name', 'Sales Ledger']
        df_helper = ledger_filterd.groupby(ledger_group_key)['Amount'].sum().reset_index()
        
        df_helper['Amount'] = df_helper['Amount'].astype(str).str.replace(r'[^\d.\-]', '', regex=True)
        df_helper['Amount'] = pd.to_numeric(df_helper['Amount'], errors='coerce').fillna(0).round(2)
        df_helper['helper1'] = (
            df_helper['Voucher Date'].astype(str) + 
            df_helper['Voucher Number'].astype(str) + 
            df_helper['Voucher Type'].astype(str) + 
            df_helper['Party Name'].astype(str) + 
            df_helper['Sales Ledger'].astype(str) + 
            df_helper['Amount'].astype(str))
        
    else:
        item_defaults = {
            'Amount': "0",
            'QTY': "0",
            'Rate': "0",
            'Discount': "0",
            'UOM': "No Unit",
            'Item Name': "No Item"
            }
        for col, default_val in item_defaults.items():
            df_item[col] = default_val

    df_ledger = pd.json_normalize(
        raw_data,
        record_path=['Ledger'],
        meta=['VOUCHERKEY', 'Voucher Date', 'Voucher Number', 'Voucher Type', 'Party Name'],
        errors='ignore',
    )

    if not df_ledger.empty:
        df_ledger['Voucher Number'] = df_ledger.get('Voucher Number', '').fillna('Blank')

        if 'Amount' not in df_ledger.columns:
            df_ledger['Amount'] = "0"

        df_ledger['currency'] = df_ledger['Amount'].astype(str).str.extract(r'(AU\$|A\$|CAD|£|€|\$)')
        df_ledger['currency'] = df_ledger['currency'].map(symbol_to_currency)
        df_ledger['currency'] = df_ledger['currency'].fillna("Unknown")
        df_ledger['Amount'] = df_ledger['Amount'].str.replace(r'[^\d.\-]', '', regex=True)
        df_ledger['Amount'] = pd.to_numeric(df_ledger['Amount'], errors='coerce').fillna(0).round(2)

        df_ledger['helper1'] = (
            df_ledger['Voucher Date'].astype(str) + 
            df_ledger['Voucher Number'].astype(str) + 
            df_ledger['Voucher Type'].astype(str) + 
            df_ledger['Party Name'].astype(str) + 
            df_ledger['LedgerName'].astype(str) + 
            df_ledger['Amount'].astype(str))

        if not df_item.empty:
            df_ledger = df_ledger.loc[~df_ledger['helper1'].isin(ledger_filterd['helper1'])]
            df_ledger = df_ledger.loc[~df_ledger['helper1'].isin(df_helper['helper1'])]
             
        pivot_df = df_ledger.pivot_table(
            values='Amount',
            index=['VOUCHERKEY', 'Voucher Date', 'Voucher Number', 'Voucher Type', 'Party Name','currency'],
            columns='LedgerName',
            aggfunc='sum',
            fill_value=0
        ).reset_index()
        # pivot_df.columns = pivot_df.columns.str.lower()
        cgst_col = [col for col in pivot_df.columns if re.match(r'^cgst\s*output', col, re.IGNORECASE)]
        sgst_col = [col for col in pivot_df.columns if re.match(r'^sgst\s*output', col, re.IGNORECASE)]
        igst_col = [col for col in pivot_df.columns if re.match(r'^igst\s*output', col, re.IGNORECASE)]
        freight_col = [col for col in pivot_df.columns if re.match(r'^freight', col, re.IGNORECASE)]
        dca_col = [col for col in pivot_df.columns if re.match(r'^dca', col, re.IGNORECASE)]
        clearing_forwarding_col = [col for col in pivot_df.columns if re.search(r'clearing\s*&?\s*forwarding', col, re.IGNORECASE)]
        tax_cols = cgst_col + sgst_col + igst_col + freight_col + dca_col + clearing_forwarding_col

        cols = ['cgst_amt', 'sgst_amt', 'igst_amt', 'other_amt', 'freight_amt', 'dca_amt', 'cf_amt']
        for col in cols:
            if col not in pivot_df.columns:
                pivot_df[col] = 0
            else:
                pivot_df[col].fillna(0, inplace=True)

        pivot_df[tax_cols] = pivot_df[tax_cols].fillna(0).astype(float)
        pivot_df['cgst_amt'] = pivot_df[cgst_col].sum(axis=1) if cgst_col else 0
        pivot_df['sgst_amt'] = pivot_df[sgst_col].sum(axis=1) if sgst_col else 0
        pivot_df['igst_amt'] = pivot_df[igst_col].sum(axis=1) if igst_col else 0
        pivot_df['freight_amt'] = pivot_df[freight_col].sum(axis=1) if freight_col else 0.0
        pivot_df['dca_amt'] = pivot_df[dca_col].sum(axis=1) if dca_col else 0.0
        pivot_df['cf_amt'] = pivot_df[clearing_forwarding_col].sum(axis=1) if clearing_forwarding_col else 0.0

        exclude_cols = set(merge_col + tax_cols + ['cgst_amt', 'sgst_amt', 'igst_amt', 'freight_amt', 'dca_amt', 'cf_amt','currency'])
        other_charge_cols = [col for col in pivot_df.columns if col not in exclude_cols and pd.api.types.is_numeric_dtype(pivot_df[col])]
        pivot_df['other_amt'] = pivot_df[other_charge_cols].sum(axis=1) if other_charge_cols else 0.0
        keep_col = merge_col + ['cgst_amt', 'sgst_amt', 'igst_amt',  'other_amt','freight_amt','dca_amt','cf_amt','currency']
        pivot_df = pivot_df[keep_col]
        df_ledger = pivot_df
    else:
        df_ledger['currency'] = 'Unknown'
        req = ['cgst_amt', 'sgst_amt', 'igst_amt',  'other_amt','freight_amt','dca_amt','cf_amt',]
        for i in req:
            if i not in df_ledger.columns:
                df_ledger[i] = 0

    df_final = pd.merge(left=df_item, right=df_ledger, how='outer', on=merge_col) 
    df_final['currency'] = df_final['currency'].fillna('Unknown')

    req_zero = ['cgst_amt', 'sgst_amt', 'igst_amt',  'other_amt','freight_amt','dca_amt','cf_amt']
    df_final[req_zero] = df_final[req_zero].fillna(0)

    df_final.columns = df_final.columns.str.lower().str.replace(" ", "_")
    cols_rename = {
        'voucher_date': 'date',
        'voucher_number': 'voucher_no',
        'party_name': 'particulars',
        'item_name': 'item',
        'uom': 'unit'
    }
    df_final = df_final.rename(columns=cols_rename)
    group_keys = ["voucherkey",'date', 'voucher_no', 'particulars']

    df_final['helper'] = df_final.groupby(group_keys).cumcount()
    for col in req_zero:
        df_final[col] = np.where(df_final['helper']==0, df_final[col], 0)
    # Format date
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        df_final['date'] = pd.to_datetime(df_final['date'], dayfirst=True, errors='coerce').dt.date
    # Ensure bill_ref_no exists

    df_final['item'] = df_final['item'].fillna("No Item")
    df_final['unit'] = df_final['unit'].fillna("No Unit")

    text_fields = ['voucher_no', 'bill_ref_no', 'particulars', 'party_group']
    for field in text_fields:
        if field not in df_final.columns:
            df_final[field] = 'Blank'
        else:
            df_final[field] = df_final[field].fillna("Blank")

    # Set material centre and currency
    df_final['material_centre'] = material_centre_name
    df_final['qty'] = pd.to_numeric(df_final['qty'], errors='coerce').fillna(0)
    
    # item amount curr find 
    df_final['extracted_symbol'] = df_final['amount'].astype(str).str.extract(r'(AU\$|A\$|CAD|£|€|\$)', expand=False)
    df_final['mapped_currency'] = df_final['extracted_symbol'].map(symbol_to_currency)
    df_final.loc[(df_final['currency'] == 'Unknown') & (df_final['mapped_currency'].notnull()), 'currency'] = df_final['mapped_currency']
    df_final.drop(columns=['extracted_symbol', 'mapped_currency'], inplace=True)
    df_final['amount'] = df_final['amount'].replace(r'[^\d.]', '', regex=True)
    df_final['amount'] = pd.to_numeric(df_final['amount'], errors='coerce').fillna(0)
    

    df_final['extracted_symbol'] = df_final['rate'].astype(str).str.extract(r'(AU\$|A\$|CAD|£|€|\$)', expand=False)
    df_final['mapped_currency'] = df_final['extracted_symbol'].map(symbol_to_currency)
    df_final.loc[(df_final['currency'] == 'Unknown') & (df_final['mapped_currency'].notnull()), 'currency'] = df_final['mapped_currency']
    df_final.drop(columns=['extracted_symbol', 'mapped_currency'], inplace=True)
    df_final['rate'] = df_final['rate'].replace(r'[^\d.]', '', regex=True)
    df_final['rate'] = pd.to_numeric(df_final['rate'], errors='coerce').fillna(0)
    df_final['currency'] = df_final['currency'].str.replace('Unknown', "").replace("", np.nan)
    df_final['currency'] = np.where(df_final['currency'].isnull(), df_final['material_centre'].map(curr), df_final['currency'])
    df_final['fcy'] = np.where(df_final['material_centre'].isin(fcy_comp), 'Yes', 'No')
    df_final['rate'] = df_final['amount'] / df_final['qty']
    df_final['rate'] = df_final['rate'].replace([np.inf, -np.inf], 0).fillna(0)

    if 'narration' not in df_final.columns:
        df_final['narration'] = None
    else:
        df_final['narration'] = df_final['narration'].where(df_final['narration'].notnull(), None)

    df_final['narration'] = df_final['narration'].str[:500]


    voucher_totals = df_final.groupby(group_keys)[['amount', 'cgst_amt', 'sgst_amt', 'igst_amt', 'other_amt','freight_amt','dca_amt','cf_amt']].sum()
    voucher_totals['total_amt'] = voucher_totals.sum(axis=1)
    voucher_totals = voucher_totals[['total_amt']].reset_index()
    df_final = df_final.merge(voucher_totals, on=group_keys, how='left')
    df_final = df_final.sort_values(by=['voucher_no', 'item'])
    df_final['total_amt'] = df_final.groupby(group_keys)['total_amt'].transform(lambda x: [x.iloc[0]] + [0] * (len(x) - 1))
    zero_fill = ['qty',"rate","amount","discount","cgst_amt","sgst_amt","igst_amt","freight_amt","dca_amt","cf_amt","other_amt","total_amt"]
    df_final[zero_fill] = df_final[zero_fill].apply(pd.to_numeric, errors='coerce')
    df_final[zero_fill] = df_final[zero_fill].fillna(0)

    # df_final = df_final.rename(columns={'bill_ref_no':"voucher_ref_no"})

    final_columns = [
        'date', 'voucher_no', 'bill_ref_no', 'voucher_type', 'particulars', 'item', 'qty', 'unit',
        'rate', 'amount', 'discount', 'cgst_amt', 'sgst_amt', 'igst_amt','freight_amt','dca_amt','cf_amt', 'other_amt', 'total_amt',
        'material_centre', 'currency', 'fcy', 'despatch_doc_no', 'port_of_loading',
        'port_of_discharge', 'narration'
    ]

    for col in final_columns:
        if col not in df_final.columns:
            df_final[col] = ''
    df_final = df_final[final_columns]
    df_final = df_final.applymap(lambda x: x.replace("_x000D_", "") if isinstance(x, str) else x)
    df_final = df_final.applymap(lambda x: x.strip("\r\n") if isinstance(x, str) else x)

    
    df_final.replace([float('inf'), float('-inf')], np.nan, inplace=True)
    return df_final

def APIPurchaseVoucher(file_path: str, material_centre_name: str):
    try:
        data = json_data_convert_amount_in_string(file_path)
        data = data['ENVELOPE']['Body']
    except Exception as e:
        print(f"Error loading or accessing data: {e}")
        return pd.DataFrame()

    try:
        for voucher in data:
            voucher.setdefault('Items', [])
            voucher.setdefault('Ledger', [])
    except Exception as e:
        print(f"Error processing vouchers: {e}")
        return pd.DataFrame()

    sample_voucher = data[0]
    meta_cols = [key for key in sample_voucher.keys() if key not in ['Items', 'Ledger']]
    merge_col = ['VOUCHERKEY', 'Voucher Date', 'Voucher Number', 'Voucher Type', 'Party Name']
    
    for key in merge_col:
        if key not in meta_cols:
            meta_cols.append(key)

    df_item = pd.json_normalize(data, record_path='Items', meta=meta_cols, errors='ignore')
    df_ledger = pd.json_normalize(
        data, 
        record_path='Ledger',
        meta=['VOUCHERKEY', 'Voucher Date', 'Voucher Number', 'Voucher Type', 'Party Name'],
        errors='ignore')

    if not df_item.empty:
        df_item['Voucher Number'] = df_item.get('Voucher Number', '').fillna('Blank')
        if 'Purchase Ledger' not in df_item.columns:
            df_item['Purchase Ledger'] = ''
        if 'Amount' not in df_item.columns:
            df_item['Amount'] = '0'   

        ledger_filterd = df_item.copy()
        ledger_filterd['Amount'] = ledger_filterd['Amount'].astype(str).str.replace(r'[^\d.\-]', '', regex=True)
        ledger_filterd['Amount'] = pd.to_numeric(ledger_filterd['Amount'], errors='coerce').fillna(0).round(2)
        ledger_filterd['helper1'] = (ledger_filterd['Voucher Date'].astype(str) + ledger_filterd['Voucher Number'].astype(str) + ledger_filterd['Voucher Type'].astype(str) + ledger_filterd['Party Name'].astype(str) + ledger_filterd['Purchase Ledger'].astype(str) + ledger_filterd['Amount'].astype(str))

        group_key = ['Voucher Date', 'Voucher Number', 'Voucher Type', 'Party Name', 'Purchase Ledger']

        df_helper = ledger_filterd.groupby(group_key)['Amount'].sum().reset_index()
        df_helper['Amount'] = df_helper['Amount'].astype(str).str.replace(r'[^\d.\-]', '', regex=True)
        df_helper['Amount'] = pd.to_numeric(df_helper['Amount'], errors='coerce').fillna(0).round(2)
        df_helper['helper1'] = (df_helper['Voucher Date'].astype(str) + df_helper['Voucher Number'].astype(str) + df_helper['Voucher Type'].astype(str) + df_helper['Party Name'].astype(str) + df_helper['Purchase Ledger'].astype(str) + df_helper['Amount'].astype(str))

    else:
        item_defaults = {'Amount': "0",'QTY': "0",'Rate': "0",'Discount': "0",'UOM': "No Unit",'Item Name': "No Item"}
        for col, default_val in item_defaults.items():
            df_item[col] = default_val

    if not df_ledger.empty:
        df_ledger['Voucher Number'] = df_ledger.get('Voucher Number', '').fillna('Blank')
        df_ledger['Amount'] = df_ledger.get('Amount', '0').fillna('0')

        df_ledger['currency'] = df_ledger['Amount'].astype(str).str.extract(r'(AU\$|A\$|CAD|£|€|\$)')
        df_ledger['currency'] = df_ledger['currency'].map(symbol_to_currency)
        df_ledger['currency'] = df_ledger['currency'].fillna("Unknown")
        df_ledger['Amount'] = df_ledger['Amount'].str.replace(r'[^\d.\-]', '', regex=True)
        df_ledger['Amount'] = pd.to_numeric(df_ledger['Amount'], errors='coerce').fillna(0).round(2)
        df_ledger['helper1'] = (df_ledger['Voucher Date'].astype(str) + df_ledger['Voucher Number'].astype(str) + df_ledger['Voucher Type'].astype(str) + df_ledger['Party Name'].astype(str) + df_ledger['LedgerName'].astype(str) + df_ledger['Amount'].astype(str))

        if not df_item.empty:
            df_ledger = df_ledger.loc[~df_ledger['helper1'].isin(ledger_filterd['helper1'])]
            df_ledger = df_ledger.loc[~df_ledger['helper1'].isin(df_helper['helper1'])]

        pivot_df = df_ledger.pivot_table(values='Amount',index=merge_col + ['currency'],columns='LedgerName',aggfunc='sum',fill_value=0).reset_index()

        cgst_col = [col for col in pivot_df.columns if re.match(r'^cgst\s*input', col, re.IGNORECASE)]
        sgst_col = [col for col in pivot_df.columns if re.match(r'^sgst\s*input', col, re.IGNORECASE)]
        igst_col = [col for col in pivot_df.columns if re.match(r'^igst\s*input', col, re.IGNORECASE)]
        freight_col = [col for col in pivot_df.columns if re.match(r'^freight', col, re.IGNORECASE)]
        dca_col = [col for col in pivot_df.columns if re.match(r'^dca', col, re.IGNORECASE)]
        clearing_forwarding_col = [col for col in pivot_df.columns if re.match(r'^clearing\s*&\s*forwarding', col, re.IGNORECASE)]

        tax_cols = cgst_col + sgst_col + igst_col + freight_col + dca_col + clearing_forwarding_col
        pivot_df[tax_cols] = pivot_df[tax_cols].fillna(0).astype(float)

        cols = ['cgst_amt', 'sgst_amt', 'igst_amt', 'other_amt', 'freight_amt', 'dca_amt', 'cf_amt']
        for col in cols:
            if col not in pivot_df.columns:
                pivot_df[col] = 0
            else:
                pivot_df[col].fillna(0, inplace=True)


        pivot_df['cgst_amt'] = pivot_df[cgst_col].sum(axis=1) if cgst_col else 0.0
        pivot_df['sgst_amt'] = pivot_df[sgst_col].sum(axis=1) if sgst_col else 0.0
        pivot_df['igst_amt'] = pivot_df[igst_col].sum(axis=1) if igst_col else 0.0
        pivot_df['freight_amt'] = pivot_df[freight_col].sum(axis=1) if freight_col else 0.0
        pivot_df['dca_amt'] = pivot_df[dca_col].sum(axis=1) if dca_col else 0.0
        pivot_df['cf_amt'] = pivot_df[clearing_forwarding_col].sum(axis=1) if clearing_forwarding_col else 0.0
        exclude_cols = set(merge_col + tax_cols + ['cgst_amt', 'sgst_amt', 'igst_amt','freight_amt','dca_amt','cf_amt','currency'])
        other_charge_cols = [col for col in pivot_df.columns if col not in exclude_cols and pd.api.types.is_numeric_dtype(pivot_df[col])]
        pivot_df['other_amt'] = pivot_df[other_charge_cols].sum(axis=1) if other_charge_cols else 0.0
        keep_col = merge_col + ['cgst_amt', 'sgst_amt', 'igst_amt',  'other_amt','freight_amt','dca_amt','cf_amt','currency']
        pivot_df = pivot_df[keep_col]
        df_ledger = pivot_df
        
    else:
        df_ledger['currency'] = 'Unknown'
        req = ['cgst_amt', 'sgst_amt', 'igst_amt',  'other_amt','freight_amt','dca_amt','cf_amt',]
        for i in req:
            if i not in df_ledger.columns:
                df_ledger[i] = 0

    if df_item.empty:
        item_col = ['Amount','QTY','Rate',"Discount"]
        for col in item_col:
            if col not in df_item.columns:
                df_item[col] = "0"

    if 'UOM' not in df_item.columns:
        df_item['UOM'] = "No Unit"
    if 'Item Name' not in df_item.columns:
        df_item['Item Name'] = "No Item"
    
    df = pd.merge(left=df_item, right=df_ledger, how='outer', on=merge_col) 
    df['currency'] = df['currency'].fillna('Unknown')

    req_zero = ['cgst_amt', 'sgst_amt', 'igst_amt',  'other_amt','freight_amt','dca_amt','cf_amt']

    df[req_zero] = df[req_zero].fillna(0)

    df.columns = df.columns.str.lower().str.replace(" ", "_")

    item_col = ['amount','qty','rate',"discount"]
    for col in item_col:
        if col not in df.columns:
            df[col] = '0'


    cols_rename = {'voucher_date': 'date','voucher_number': 'voucher_no','party_name': 'particulars','item_name': 'item','uom': 'unit'}
    df = df.rename(columns=cols_rename)

    group_keys = ['voucherkey', 'date', 'voucher_no', 'particulars']
    df['helper'] = df.groupby(group_keys).cumcount()
    for col in req_zero:
        df[col] = np.where(df['helper']==0, df[col], 0)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce').dt.date

    df['material_centre'] = material_centre_name

    df['extracted_symbol'] = df['amount'].astype(str).str.extract(r'(AU\$|A\$|CAD|£|€|\$)', expand=False)
    df['mapped_currency'] = df['extracted_symbol'].map(symbol_to_currency)
    df.loc[(df['currency'] == 'Unknown') & (df['mapped_currency'].notnull()), 'currency'] = df['mapped_currency']
    df.drop(columns=['extracted_symbol', 'mapped_currency'], inplace=True)
    df['amount'] = df['amount'].replace(r'[^\d.]', '', regex=True)
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)

    # rate extract curr
    df['extracted_symbol'] = df['rate'].astype(str).str.extract(r'(AU\$|A\$|CAD|£|€|\$)', expand=False)
    df['mapped_currency'] = df['extracted_symbol'].map(symbol_to_currency)
    df.loc[(df['currency'] == 'Unknown') & (df['mapped_currency'].notnull()), 'currency'] = df['mapped_currency']
    df.drop(columns=['extracted_symbol', 'mapped_currency'], inplace=True)

    df['rate'] = df['rate'].replace(r'[^\d.]', '', regex=True)
    df['rate'] = pd.to_numeric(df['rate'], errors='coerce').fillna(0)
    df['qty'] = pd.to_numeric(df['qty'], errors='coerce').fillna(0)
    df['discount'] = pd.to_numeric(df['discount'], errors='coerce').fillna(0)

    df['currency'] = df['currency'].str.replace('Unknown', "").replace("", np.nan)
    df['currency'] = np.where(df['currency'].isnull(), df['material_centre'].map(curr), df['currency'])
    df['rate'] = df['amount'] / df['qty']
    df['rate'] = df['rate'].replace([np.inf, -np.inf], 0).fillna(0)

    df['fcy'] = np.where(df['material_centre'].isin(fcy_comp), 'Yes', 'No')

    for field in ['voucher_no', 'particulars']:
        if field in df.columns:
            df[field] = df[field].fillna('Blank')
        else:
            df[field] = 'Blank'

    for field, default_value in [('item', 'No Item'), ('unit', 'No Unit')]:
        if field in df.columns:
            df[field] = df[field].fillna(default_value)
        else:
            df[field] = default_value

    if 'narration' not in df.columns:
        df['narration'] = None
    else:
        df['narration'] = df['narration'].where(df['narration'].notnull(), None)

    number_cols = ['gst_rate', 'discount', 'rate', 'qty', 'amount','freight_amt', 'dca_amt', 'cf_amt','cgst_amt', 'sgst_amt', 'igst_amt', 'other_amt']
    for col in number_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        else:
            df[col] = 0
    
    voucher_totals = df.groupby(group_keys)[['cgst_amt', 'sgst_amt', 'igst_amt', 'freight_amt','dca_amt','cf_amt', 'other_amt','amount']].sum()
    voucher_totals['total_amt'] = voucher_totals.sum(axis=1)
    df = df.merge(voucher_totals[['total_amt']].reset_index(), on=group_keys, how='left')

    df['total_amt'] = df.groupby(group_keys)['total_amt'].transform(lambda x: [x.iloc[0]] + [0] * (len(x) - 1))
    df = df.sort_values(by=['voucher_no', 'item'])

    final_col = ['date','voucher_no','voucher_type','particulars','party_gstin','item','unit','qty','rate','amount','cgst_amt', 'sgst_amt', 'igst_amt',"discount",'freight_amt','dca_amt','cf_amt','other_amt','total_amt','material_centre','currency','fcy','narration']

    for col in final_col:
        if col not in df.columns:
            df[col] = ''

    df['narration'] = df['narration'].str[:500]
    df = df[final_col]
    df = df.applymap(lambda x: x.replace("_x000D_", "") if isinstance(x, str) else x)
    df = df.applymap(lambda x: x.strip("\r\n") if isinstance(x, str) else x)

    return df

def APIPurchaseReturnVoucher(file_path: str, material_centre_name: str):
    try:
        data = json_data_convert_amount_in_string(file_path)
        data = data['ENVELOPE']['Body']
    except Exception as e:
        print(f"Error loading or accessing data: {e}")
        return pd.DataFrame()

    try:
        for voucher in data:
            voucher.setdefault('Items', [])
            voucher.setdefault('Ledger', [])
    except Exception as e:
        print(f"Error processing vouchers: {e}")
        return pd.DataFrame()

    sample_voucher = data[0]
    meta_cols = [key for key in sample_voucher.keys() if key not in ['Items', 'Ledger']]
    merge_col = ['VOUCHERKEY', 'Voucher Date', 'Voucher Number', 'Voucher Type', 'Party Name']
    for key in merge_col:
        if key not in meta_cols:
            meta_cols.append(key)

    df_item = pd.json_normalize(data, record_path='Items', meta=meta_cols, errors='ignore')

    df_ledger = pd.json_normalize(
        data, 
        record_path='Ledger',
        meta=['VOUCHERKEY', 'Voucher Date', 'Voucher Number', 'Voucher Type', 'Party Name'],
        errors='ignore')
    
    if not df_item.empty:
        df_item['Voucher Number'] = df_item.get('Voucher Number', '').fillna('Blank')
        if 'Purchase Ledger' not in df_item.columns:
            df_item['Purchase Ledger'] = ''
        if 'Amount' not in df_item.columns:
            df_item['Amount'] = '0'   

        ledger_filterd = df_item.copy()
        ledger_filterd['Amount'] = ledger_filterd['Amount'].astype(str).str.replace(r'[^\d.\-]', '', regex=True)
        ledger_filterd['Amount'] = pd.to_numeric(ledger_filterd['Amount'], errors='coerce').fillna(0).round(2)
        
        ledger_filterd['helper1'] = (
            ledger_filterd['Voucher Date'].astype(str) + 
            ledger_filterd['Voucher Number'].astype(str) + 
            ledger_filterd['Voucher Type'].astype(str) + 
            ledger_filterd['Party Name'].astype(str) + 
            ledger_filterd['Purchase Ledger'].astype(str) + 
            ledger_filterd['Amount'].astype(str)
            )
        helper_group = ['Voucher Date', 'Voucher Number', 'Voucher Type', 'Party Name', 'Purchase Ledger']

        df_helper = ledger_filterd.groupby(helper_group)['Amount'].sum().reset_index()
        df_helper['Amount'] = df_helper['Amount'].astype(str).str.replace(r'[^\d.\-]', '', regex=True)
        df_helper['Amount'] = pd.to_numeric(df_helper['Amount'], errors='coerce').fillna(0).round(2)

        df_helper['helper1'] = (
            df_helper['Voucher Date'].astype(str) + 
            df_helper['Voucher Number'].astype(str) + 
            df_helper['Voucher Type'].astype(str) + 
            df_helper['Party Name'].astype(str) + 
            df_helper['Purchase Ledger'].astype(str) + 
            df_helper['Amount'].astype(str)
            )

    else:
        item_defaults = {'Amount': "0",'QTY': "0",'Rate': "0",'Discount': "0",'UOM': "No Unit",'Item Name': "No Item"}
        for col, default_val in item_defaults.items():
            df_item[col] = default_val

    if not df_ledger.empty:

        df_ledger['Voucher Number'] = df_ledger.get('Voucher Number', '').fillna('Blank')
        df_ledger['Amount'] = df_ledger.get('Amount', '0').fillna('0')
        df_ledger['currency'] = df_ledger['Amount'].astype(str).str.extract(r'(AU\$|A\$|CAD|£|€|\$)')
        df_ledger['currency'] = df_ledger['currency'].map(symbol_to_currency)
        df_ledger['currency'] = df_ledger['currency'].fillna("Unknown")
        df_ledger['Amount'] = df_ledger['Amount'].str.replace(r'[^\d.\-]', '', regex=True)
        df_ledger['Amount'] = pd.to_numeric(df_ledger['Amount'], errors='coerce').fillna(0).round(2)
        
        df_ledger['helper1'] = (
            df_ledger['Voucher Date'].astype(str) + 
            df_ledger['Voucher Number'].astype(str) + 
            df_ledger['Voucher Type'].astype(str) + 
            df_ledger['Party Name'].astype(str) + 
            df_ledger['LedgerName'].astype(str) + 
            df_ledger['Amount'].astype(str)
            )

        if not df_item.empty:
            df_ledger = df_ledger.loc[~df_ledger['helper1'].isin(ledger_filterd['helper1'])]
            df_ledger = df_ledger.loc[~df_ledger['helper1'].isin(df_helper['helper1'])]

        pivot_df = df_ledger.pivot_table(
            values='Amount',
            index=merge_col + ['currency'],
            columns='LedgerName',
            aggfunc='sum',
            fill_value=0
        ).reset_index()

        cgst_col = [col for col in pivot_df.columns if re.match(r'^cgst\s*input', col, re.IGNORECASE)]
        sgst_col = [col for col in pivot_df.columns if re.match(r'^sgst\s*input', col, re.IGNORECASE)]
        igst_col = [col for col in pivot_df.columns if re.match(r'^igst\s*input', col, re.IGNORECASE)]
        freight_col = [col for col in pivot_df.columns if re.match(r'^freight', col, re.IGNORECASE)]
        dca_col = [col for col in pivot_df.columns if re.match(r'^dca', col, re.IGNORECASE)]
        clearing_forwarding_col = [col for col in pivot_df.columns if re.match(r'^clearing\s*&\s*forwarding', col, re.IGNORECASE)]
        tax_cols = cgst_col + sgst_col + igst_col + freight_col + dca_col + clearing_forwarding_col

        cols = ['cgst_amt', 'sgst_amt', 'igst_amt', 'other_amt', 'freight_amt', 'dca_amt', 'cf_amt']
        for col in cols:
            if col not in pivot_df.columns:
                pivot_df[col] = 0
            else:
                pivot_df[col].fillna(0, inplace=True)


        pivot_df[tax_cols] = pivot_df[tax_cols].fillna(0).astype(float)
        pivot_df['cgst_amt'] = pivot_df[cgst_col].sum(axis=1) if cgst_col else 0.0
        pivot_df['sgst_amt'] = pivot_df[sgst_col].sum(axis=1) if sgst_col else 0.0
        pivot_df['igst_amt'] = pivot_df[igst_col].sum(axis=1) if igst_col else 0.0
        pivot_df['freight_amt'] = pivot_df[freight_col].sum(axis=1) if freight_col else 0.0
        pivot_df['dca_amt'] = pivot_df[dca_col].sum(axis=1) if dca_col else 0.0
        pivot_df['cf_amt'] = pivot_df[clearing_forwarding_col].sum(axis=1) if clearing_forwarding_col else 0.0
        exclude_cols = set(merge_col + tax_cols + ['cgst_amt', 'sgst_amt', 'igst_amt','freight_amt','dca_amt','cf_amt','currency'])
        other_charge_cols = [col for col in pivot_df.columns if col not in exclude_cols and pd.api.types.is_numeric_dtype(pivot_df[col])]
        pivot_df['other_amt'] = pivot_df[other_charge_cols].sum(axis=1) if other_charge_cols else 0.0
        keep_col = merge_col + ['cgst_amt', 'sgst_amt', 'igst_amt',  'other_amt','freight_amt','dca_amt','cf_amt','currency']
        pivot_df = pivot_df[keep_col]
        df_ledger = pivot_df
    else:
        df_ledger['currency'] = 'Unknown'
        req = ['cgst_amt', 'sgst_amt', 'igst_amt',  'other_amt','freight_amt','dca_amt','cf_amt',]
        for i in req:
            if i not in df_ledger.columns:
                df_ledger[i] = 0.0

    if df_item.empty:
        item_col = ['Amount','QTY','Rate',"Discount"]
        for col in item_col:
            if col not in df_item.columns:
                df_item[col] = "0"

    if 'UOM' not in df_item.columns:
        df_item['UOM'] = "No Unit"
    if 'Item Name' not in df_item.columns:
        df_item['Item Name'] = "No Item"
    
    df = pd.merge(left=df_item, right=df_ledger, how='outer', on=merge_col) 
    df['currency'] = df['currency'].fillna('Unknown')
    req_zero = ['cgst_amt', 'sgst_amt', 'igst_amt',  'other_amt','freight_amt','dca_amt','cf_amt']
    df[req_zero] = df[req_zero].fillna(0)

    df.columns = df.columns.str.lower().str.replace(" ", "_")

    item_col = ['amount','qty','rate',"discount"]
    for col in item_col:
        if col not in df.columns:
            df[col] = '0'

    cols_rename = {
        'voucher_date': 'date',
        'voucher_number': 'voucher_no',
        'party_name': 'particulars',
        'item_name': 'item',
        'uom': 'unit'}
    df = df.rename(columns=cols_rename)

    group_keys = ["voucherkey",'date', 'voucher_no', 'particulars']
    df['helper'] = df.groupby(group_keys).cumcount()
    for col in req_zero:
        df[col] = np.where(df['helper']==0, df[col], 0)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce').dt.date

    df['material_centre'] = material_centre_name

    # item amount curr find 
    df['extracted_symbol'] = df['amount'].astype(str).str.extract(r'(AU\$|A\$|CAD|£|€|\$)', expand=False)
    df['mapped_currency'] = df['extracted_symbol'].map(symbol_to_currency)
    df.loc[(df['currency'] == 'Unknown') & (df['mapped_currency'].notnull()), 'currency'] = df['mapped_currency']
    df.drop(columns=['extracted_symbol', 'mapped_currency'], inplace=True)
    df['amount'] = df['amount'].replace(r'[^\d.]', '', regex=True)
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)

    df['qty'] = pd.to_numeric(df['qty'], errors='coerce').fillna(0)

    # rate extract curr
    df['extracted_symbol'] = df['rate'].astype(str).str.extract(r'(AU\$|A\$|CAD|£|€|\$)', expand=False)
    df['mapped_currency'] = df['extracted_symbol'].map(symbol_to_currency)
    df.loc[(df['currency'] == 'Unknown') & (df['mapped_currency'].notnull()), 'currency'] = df['mapped_currency']
    df.drop(columns=['extracted_symbol', 'mapped_currency'], inplace=True)
    df['rate'] = df['rate'].replace(r'[^\d.]', '', regex=True)
    df['rate'] = pd.to_numeric(df['rate'], errors='coerce').fillna(0)

    df['currency'] = df['currency'].str.replace('Unknown', "").replace("", np.nan)
    df['currency'] = np.where(df['currency'].isnull(), df['material_centre'].map(curr), df['currency'])
    df['fcy'] = np.where(df['material_centre'].isin(fcy_comp), 'Yes', 'No')
    df['rate'] = df['amount'] / df['qty']
    df['rate'] = df['rate'].replace([np.inf, -np.inf], 0).fillna(0)

    for field in ['voucher_no', 'particulars']:
        if field in df.columns:
            df[field] = df[field].fillna('Blank')
        else:
            df[field] = 'Blank'

    for field, default_value in [('item', 'No Item'), ('unit', 'No Unit')]:
        if field in df.columns:
            df[field] = df[field].fillna(default_value)
        else:
            df[field] = default_value


    if 'narration' not in df.columns:
        df['narration'] = None
    else:
        df['narration'] = df['narration'].where(df['narration'].notnull(), None)

    number_cols = ['gst_rate', 'discount', 'rate', 'qty','amount','freight_amt','dca_amt','cf_amt']
    for col in number_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        else:
            df[col] = 0


    voucher_totals = df.groupby(group_keys)[['cgst_amt', 'sgst_amt', 'igst_amt', 'freight_amt','dca_amt','cf_amt', 'other_amt','amount']].sum()
    voucher_totals['total_amt'] = voucher_totals.sum(axis=1)
    df = df.merge(voucher_totals[['total_amt']].reset_index(), on=group_keys, how='left')
    df['total_amt'] = df.groupby(group_keys)['total_amt'].transform(lambda x: [x.iloc[0]] + [0] * (len(x) - 1))

    df = df.sort_values(by=['voucher_no', 'item'])

    final_col = ['date','voucher_no','voucher_type','particulars','party_gstin','item','unit','qty','rate','amount','cgst_amt', 'sgst_amt', 'igst_amt','freight_amt','dca_amt','cf_amt','other_amt','total_amt','material_centre','currency','fcy','narration']
    
    minus = ['cgst_amt', 'sgst_amt', 'igst_amt','other_amt','total_amt','freight_amt','dca_amt','cf_amt']
    df[minus] = df[minus] * -1
    df[minus] = df[minus].replace(-0, 0)
    df['narration'] = df['narration'].str[:500]

    for col in final_col:
        if col not in df.columns:
            df[col] = ''
    df = df[final_col]
    df = df.applymap(lambda x: x.replace("_x000D_", "") if isinstance(x, str) else x)
    df = df.applymap(lambda x: x.strip("\r\n") if isinstance(x, str) else x)


    return df

def APISalesReturnVoucher(file_path: str, material_centre_name: str):
    try:
        data = json_data_convert_amount_in_string(file_path)
        raw_data = data['ENVELOPE']['Body']
    except Exception as e:
        print(f"json convert error {e}")
    
    for voucher in raw_data:
        voucher.setdefault('Items', [])
        voucher.setdefault('Ledger', [])

    sample_voucher = raw_data[0]
    meta_cols = [key for key in sample_voucher.keys() if key not in ['Items', 'Ledger']]
    merge_col = ['VOUCHERKEY', 'Voucher Date', 'Voucher Number', 'Voucher Type', 'Party Name']

    for key in merge_col:
        if key not in meta_cols:
            meta_cols.append(key)

    df_item = pd.json_normalize(raw_data, errors='ignore', record_path='Items', meta=meta_cols)

    df_ledger = pd.json_normalize(raw_data,record_path=['Ledger'],meta=['VOUCHERKEY', 'Voucher Date', 'Voucher Number', 'Voucher Type', 'Party Name'], errors='ignore',)
    
    if not df_item.empty:
        df_item['Voucher Number'] = df_item.get('Voucher Number', '').fillna('Blank')

        if 'Sales Ledger' not in df_item.columns:
            df_item['Sales Ledger'] = '' 

        if 'Amount' not in df_item.columns:
            df_item['Amount'] = '0' 

        ledger_filterd = df_item.copy()

        ledger_filterd['Amount'] = ledger_filterd['Amount'].astype(str).str.replace(r'[^\d.\-]', '', regex=True)
        ledger_filterd['Amount'] = pd.to_numeric(ledger_filterd['Amount'], errors='coerce').fillna(0).round(2)

        ledger_filterd['helper1'] = (

            ledger_filterd['Voucher Date'].astype(str) + 
            ledger_filterd['Voucher Number'].astype(str) + 
            ledger_filterd['Voucher Type'].astype(str) + 
            ledger_filterd['Party Name'].astype(str) + 
            ledger_filterd['Sales Ledger'].astype(str) + 
            ledger_filterd['Amount'].astype(str)
            )

        group_key = ['Voucher Date', 'Voucher Number', 'Voucher Type', 'Party Name', 'Sales Ledger']
        df_helper = ledger_filterd.groupby(group_key)['Amount'].sum().reset_index()
        
        df_helper['Amount'] = df_helper['Amount'].astype(str).str.replace(r'[^\d.\-]', '', regex=True)
        df_helper['Amount'] = pd.to_numeric(df_helper['Amount'], errors='coerce').fillna(0).round(2)
        df_helper['helper1'] = (
            df_helper['Voucher Date'].astype(str) + 
            df_helper['Voucher Number'].astype(str) + 
            df_helper['Voucher Type'].astype(str) + 
            df_helper['Party Name'].astype(str) + 
            df_helper['Sales Ledger'].astype(str) + 
            df_helper['Amount'].astype(str)
            )
    else:
        item_defaults = {'Amount': "0",'QTY': "0",'Rate': "0",'Discount': "0",'UOM': "No Unit",'Item Name': "No Item"}
        for col, default_val in item_defaults.items():
            df_item[col] = default_val


    if not df_ledger.empty:
        df_ledger['Voucher Number'] = df_ledger.get('Voucher Number', '').fillna('Blank')

        if 'Amount' not in df_ledger.columns:
            df_ledger['Amount'] = "0"

        df_ledger['currency'] = df_ledger['Amount'].astype(str).str.extract(r'(AU\$|A\$|CAD|£|€|\$)')
        df_ledger['currency'] = df_ledger['currency'].map(symbol_to_currency)
        df_ledger['currency'] = df_ledger['currency'].fillna("Unknown")
        df_ledger['Amount'] = df_ledger['Amount'].str.replace(r'[^\d.\-]', '', regex=True)
        df_ledger['Amount'] = pd.to_numeric(df_ledger['Amount'], errors='coerce').fillna(0).round(2)

        df_ledger['helper1'] = (
            df_ledger['Voucher Date'].astype(str) + 
            df_ledger['Voucher Number'].astype(str) + 
            df_ledger['Voucher Type'].astype(str) + 
            df_ledger['Party Name'].astype(str) + 
            df_ledger['LedgerName'].astype(str) + 
            df_ledger['Amount'].astype(str)
            )
    
        if not df_item.empty:
            df_ledger = df_ledger.loc[~df_ledger['helper1'].isin(ledger_filterd['helper1'])]
            df_ledger = df_ledger.loc[~df_ledger['helper1'].isin(df_helper['helper1'])]

        pivot_df = df_ledger.pivot_table(
            values='Amount',
            index=['VOUCHERKEY', 'Voucher Date', 'Voucher Number', 'Voucher Type', 'Party Name','currency'],
            columns='LedgerName',
            aggfunc='sum',
            fill_value=0
            ).reset_index()  

        cgst_col = [col for col in pivot_df.columns if re.match(r'^cgst\s*output', col, re.IGNORECASE)]
        sgst_col = [col for col in pivot_df.columns if re.match(r'^sgst\s*output', col, re.IGNORECASE)]
        igst_col = [col for col in pivot_df.columns if re.match(r'^igst\s*output', col, re.IGNORECASE)]

        freight_col = [col for col in pivot_df.columns if re.match(r'^freight', col, re.IGNORECASE)]
        dca_col = [col for col in pivot_df.columns if re.match(r'^dca', col, re.IGNORECASE)]
        clearing_forwarding_col = [col for col in pivot_df.columns if re.match(r'^clearing\s*&\s*forwarding', col, re.IGNORECASE)]

        tax_cols = cgst_col + sgst_col + igst_col + freight_col + dca_col + clearing_forwarding_col
    
        pivot_df[tax_cols] = pivot_df[tax_cols].fillna(0).astype(float)

        pivot_df['cgst_amt'] = pivot_df[cgst_col].sum(axis=1) if cgst_col else 0
        pivot_df['sgst_amt'] = pivot_df[sgst_col].sum(axis=1) if sgst_col else 0
        pivot_df['igst_amt'] = pivot_df[igst_col].sum(axis=1) if igst_col else 0

        for col in ['freight_amt', 'dca_amt', 'cf_amt']:
            if col not in pivot_df.columns:
                pivot_df[col] = 0.0

        pivot_df['freight_amt'] = pivot_df[freight_col].sum(axis=1) if freight_col else 0.0
        pivot_df['dca_amt'] = pivot_df[dca_col].sum(axis=1) if dca_col else 0.0
        pivot_df['cf_amt'] = pivot_df[clearing_forwarding_col].sum(axis=1) if clearing_forwarding_col else 0.0

        exclude_cols = set(merge_col + tax_cols + ['cgst_amt', 'sgst_amt', 'igst_amt','freight_amt','dca_amt','cf_amt','currency'])

        other_charge_cols = [col for col in pivot_df.columns if col not in exclude_cols and pd.api.types.is_numeric_dtype(pivot_df[col])]
        pivot_df['other_amt'] = pivot_df[other_charge_cols].sum(axis=1) if other_charge_cols else 0.0

        keep_col = merge_col + ['cgst_amt', 'sgst_amt', 'igst_amt',  'other_amt','freight_amt','dca_amt','cf_amt','currency']
        pivot_df = pivot_df[keep_col]
        df_ledger = pivot_df
    else:
        df_ledger['currency'] = 'Unknown'
        req = ['cgst_amt', 'sgst_amt', 'igst_amt',  'other_amt','freight_amt','dca_amt','cf_amt',]
        for i in req:
            if i not in df_ledger.columns:
                df_ledger[i] = 0.0

    if df_item.empty:
        item_col = ['Amount','QTY','Rate',"Discount"]
        for col in item_col:
            if col not in df_item.columns:
                df_item[col] = "0"

    if 'UOM' not in df_item.columns:
        df_item['UOM'] = "No Unit"
    if 'Item Name' not in df_item.columns:
        df_item['Item Name'] = "No Item"

    df_final = pd.merge(left=df_item, right=df_ledger, how='outer', on=merge_col) 
    df_final['currency'] = df_final['currency'].fillna('Unknown')

    req_zero = ['cgst_amt', 'sgst_amt', 'igst_amt',  'other_amt','freight_amt','dca_amt','cf_amt']
    df_final[req_zero] = df_final[req_zero].fillna(0)

    df_final.columns = df_final.columns.str.lower().str.replace(" ", "_")

    cols_rename = {'voucher_date': 'date','voucher_number': 'voucher_no','party_name': 'particulars','item_name': 'item','uom': 'unit'}
    df_final = df_final.rename(columns=cols_rename)

    group_keys_cumcount = ["voucherkey",'date', 'voucher_no', 'particulars']
    df_final['helper'] = df_final.groupby(group_keys_cumcount).cumcount()
    for col in req_zero:
        df_final[col] = np.where(df_final['helper']==0, df_final[col], 0)
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        df_final['date'] = pd.to_datetime(df_final['date'], dayfirst=True, errors='coerce').dt.date

    if 'bill_ref_no' not in df_final.columns:
        df_final['bill_ref_no'] = "Blank"
    else:
        df_final['bill_ref_no'] = df_final['bill_ref_no'].fillna("Blank")

    df_final['material_centre'] = material_centre_name

    df_final['extracted_symbol'] = df_final['amount'].astype(str).str.extract(r'(AU\$|A\$|CAD|£|€|\$)', expand=False)
    df_final['mapped_currency'] = df_final['extracted_symbol'].map(symbol_to_currency)
    df_final.loc[(df_final['currency'] == 'Unknown') & (df_final['mapped_currency'].notnull()), 'currency'] = df_final['mapped_currency']
    df_final.drop(columns=['extracted_symbol', 'mapped_currency'], inplace=True)
    df_final['amount'] = df_final['amount'].replace(r'[^\d.]', '', regex=True)

    df_final['amount'] = pd.to_numeric(df_final['amount'], errors='coerce')
    df_final['qty'] = pd.to_numeric(df_final['qty'], errors='coerce')

    df_final['currency'] = df_final['currency'].str.replace('Unknown', "").replace("", np.nan)
    df_final['currency'] = np.where(df_final['currency'].isnull(), df_final['material_centre'].map(curr), df_final['currency'])
    
    df_final['fcy'] = np.where(df_final['material_centre'].isin(fcy_comp), 'Yes', 'No')
    df_final['rate'] = df_final['amount'] / df_final['qty']
    df_final['rate'] = df_final['rate'].replace([np.inf, -np.inf], 0).fillna(0)
    df_final['item'] = df_final['item'].fillna("No Item")
    df_final['unit'] = df_final['unit'].fillna("No Unit")

    text_fields = ['voucher_no', 'bill_ref_no', 'particulars', 'party_group']
    for field in text_fields:
        if field not in df_final.columns:
            df_final[field] = 'Blank'
        else:
            df_final[field] = df_final[field].fillna("Blank")

    if 'narration' not in df_final.columns:
        df_final['narration'] = None
    else:
        df_final['narration'] = df_final['narration'].where(df_final['narration'].notnull(), None)

    for col in ['cgst_amt', 'sgst_amt', 'igst_amt', 'other_amt','freight_amt','dca_amt','cf_amt','amount','distance', 'gst_rate',  'discount', 'rate', 'qty',]:
        if col not in df_final.columns:
            df_final[col] = 0.0
        else:
            df_final[col] = pd.to_numeric(df_final[col], errors='coerce').fillna(0)

    voucher_totals = df_final.groupby(group_keys_cumcount)[['amount', 'cgst_amt', 'sgst_amt', 'igst_amt', 'other_amt','freight_amt','dca_amt','cf_amt']].sum()
    voucher_totals['total_amt'] = voucher_totals.sum(axis=1)
    voucher_totals = voucher_totals[['total_amt']].reset_index()
    
    df_final = df_final.merge(voucher_totals, on=group_keys_cumcount, how='left')
    df_final = df_final.sort_values(by=['voucher_no', 'item'])
    df_final['total_amt'] = df_final.groupby(group_keys_cumcount)['total_amt'].transform(lambda x: [x.iloc[0]] + [0] * (len(x) - 1))

    final_columns = [
        'date', 'voucher_no', 'bill_ref_no', 'voucher_type', 'particulars', 'item', 'qty', 'unit',
        'rate', 'amount', 'discount', 'cgst_amt', 'sgst_amt', 'igst_amt','freight_amt','dca_amt','cf_amt', 'other_amt', 'total_amt',
        'material_centre', 'currency', 'fcy', 'narration']

    for col in final_columns:
        if col not in df_final.columns:
            df_final[col] = ''

    df_final['narration'] = df_final['narration'].str[:500]
    df_final = df_final[final_columns]
    df_final = df_final.applymap(lambda x: x.replace("_x000D_", "") if isinstance(x, str) else x)
    df_final = df_final.applymap(lambda x: x.strip("\r\n") if isinstance(x, str) else x)

    return df_final

def APIMaster(file_path: str, material_centre_name: str):
    try:
        data = json_data_convert_amount_in_string(file_path)
        raw_data = data["ENVELOPE"]["Body"]
    except Exception as e:
        print(f"Error extracting raw data: {e}")
        return None
    
    df = pd.json_normalize(raw_data,errors='ignore')
    final_columns = [
        "Party Name", "Party Alias", "Parent", "Address", "Address-2", "Address-3", "Address-4",
        "State", "Country", "Pin code", "PAN", "Registration Type", "GSTIN", "Contact Person",
        "Mobile", "Phone No.", "Email", "Email CC", "Credit Period"
        ]
    
    
    for col in final_columns:
        if col not in df.columns:
            df[col] = None

    df = df[final_columns]

    df.columns = df.columns.str.lower().str.replace(" ","_").str.replace(".","").str.replace("-","_")

    df["material_centre"] = material_centre_name
    
    df['fcy'] = np.where(df['material_centre'].isin(fcy_comp), 'Yes', 'No')
    # when exported error


    for col in ['party_name', 'party_alias', 'parent', 'address', 'address_2', 'address_3', 'address_4']:
        df[col] = df[col].apply(clean_string)

    df = df.applymap(lambda x: x.replace("_x000D_", "") if isinstance(x, str) else x)
    df = df.applymap(lambda x: x.strip("\r\n") if isinstance(x, str) else x)



    df = df.where(pd.notnull(df), None)

    return df

def APIItems(file_path: str, material_centre_name: str):
    try:
        data = json_data_convert_amount_in_string(file_path)
        raw_data = data["ENVELOPE"]["Body"]
    except Exception as e:
        print(f"Error extracting raw data: {e}")
        return None

    try:
        df = pd.json_normalize(raw_data, errors='ignore')
        if df.empty:
            print("No data found in JSON.")
            return None

        df.rename(columns=lambda x: x.replace("Supplay", "Supply"), inplace=True)
        df.columns = df.columns.str.lower().str.replace(" ", "_")

        expected_columns = [
            "item_name", "item_alias", "parent", "unit",
            "cgst", "sgst", "igst", "type_of_supply"
        ]
        for col in expected_columns:
            if col not in df.columns:
                df[col] = None

        df = df[expected_columns]

        number_cols = ['cgst', 'sgst', 'igst']
        df[number_cols] = df[number_cols].apply(pd.to_numeric, errors='coerce').fillna(0)

        df['unit'] = df['unit'].fillna("No Unit")
        

        df["material_centre"] = material_centre_name
        
        df['fcy'] = np.where(df['material_centre'].isin(fcy_comp), 'Yes', 'No')
        df = df.applymap(lambda x: x.replace("_x000D_", "") if isinstance(x, str) else x)
        df = df.applymap(lambda x: x.strip("\r\n") if isinstance(x, str) else x)

        cols = ['item_name', 'item_alias', 'parent', 'unit']
        for col in cols:
            if col in df.columns:
                df[col] = df[col].apply(clean_string)
            else:
                print(f"Column '{col}' not found")
    

        return df

    except Exception as e:
        print(f"Error during data transformation: {e}")
        return None

def APIReceiptVoucher(file_path: str, material_centre_name: str):
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

    final_cols = [
        'date', 'voucher_no', 'party_name', 'inr_amount',
        'forex_amount', 'rate_of_exchange', 'amount_type',
        'currency', 'fcy', 'material_centre','narration'
    ]
    


    for col in final_cols:
        if col not in df.columns:
            df[col] = ''

    df['narration'] = df['narration'].str[:500]

    df = df.applymap(lambda x: x.replace("_x000D_", "") if isinstance(x, str) else x)
    df = df.applymap(lambda x: x.strip("\r\n") if isinstance(x, str) else x)

    df = df[final_cols]

    return df




class TallyDataProcessor:
    def __init__(self, excel_file_path) -> None:
        self.excel_file_path = excel_file_path      

    
    def clean_and_transform(self):
        df = None

        company_code = get_compname_tally(self.excel_file_path)
        report_type = get_filename_tally(self.excel_file_path)

        if report_type in ['sales']:
             df = APISalesVoucher(file_path=self.excel_file_path, material_centre_name=company_code)

        if report_type in ['sales-return']:
             df = APISalesReturnVoucher(file_path=self.excel_file_path, material_centre_name=company_code)

        if report_type in ['purchase']:
             df = APIPurchaseVoucher(file_path=self.excel_file_path, material_centre_name=company_code)

        if report_type in ['purchase-return']:
             df = APIPurchaseReturnVoucher(file_path=self.excel_file_path, material_centre_name=company_code)

        if report_type in ['item']:
             df = APIItems(file_path=self.excel_file_path, material_centre_name=company_code)

        if report_type in ['master']:
             df = APIMaster(file_path=self.excel_file_path, material_centre_name=company_code)

        if report_type in ['receipt']:
             df = APIReceiptVoucher(file_path=self.excel_file_path, material_centre_name=company_code)

        # if report_type in ['payments']:
        #      df = (file_path=self.excel_file_path, material_centre_name=company_code)
        # if report_type in ['journal']:
        #      df = (file_path=self.excel_file_path, material_centre_name=company_code)
        
        
        
        
        
        if df is None:
            logger.error("Dataframe is None!")
            return None

        return df



