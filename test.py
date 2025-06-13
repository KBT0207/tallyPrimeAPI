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
    
    try:

        for voucher in raw_data:
            voucher.setdefault('Items', [])
            voucher.setdefault('Ledger', [])

        sample_voucher = raw_data[0]
        meta_cols = [key for key in sample_voucher.keys() if key not in ['Items', 'Ledger']]
        merge_col = ['VOUCHERKEY', 'Voucher Date', 'Voucher Number', 'Voucher Type', 'Party Name']

        df = pd.json_normalize(raw_data, errors='ignore', record_path='Items', meta=meta_cols)

        df_ledger = pd.json_normalize(
            raw_data,
            record_path=['Ledger'],
            meta=['VOUCHERKEY', 'Voucher Date', 'Voucher Number', 'Voucher Type', 'Party Name'],
            errors='ignore',
        )
        if not df_ledger.empty:
            df_ledger['currency'] = df_ledger['Amount'].astype(str).str.extract(r'(AU\$|CAD|£|€|\$)')
            df_ledger['currency'] = df_ledger['currency'].map(symbol_to_currency)
            df_ledger['currency'] = df_ledger['currency'].fillna("Unknown")
            df_ledger['Amount'] = df_ledger['Amount'].str.replace(r'[^\d.\-]', '', regex=True)
            df_ledger['Amount'] = pd.to_numeric(df_ledger['Amount'], errors='coerce')

            pivot_df = df_ledger.pivot_table(
                values='Amount',
                index=['VOUCHERKEY', 'Voucher Date', 'Voucher Number', 'Voucher Type', 'Party Name','currency'],
                columns='LedgerName',
                aggfunc='sum',
                fill_value=0
            ).reset_index()  

            cgst_col = [col for col in pivot_df.columns if col.lower().startswith('cgst output')]
            sgst_col = [col for col in pivot_df.columns if col.lower().startswith('sgst output')]
            igst_col = [col for col in pivot_df.columns if col.lower().startswith('igst output')]

            freight_col = [col for col in pivot_df.columns if col.lower().startswith('freight')]
            dca_col = [col for col in pivot_df.columns if col.lower().startswith("dca")]
            clearing_forwarding_col = [col for col in pivot_df.columns if col.lower().startswith("clearing & forwarding")]

            tax_cols = cgst_col + sgst_col + igst_col + freight_col + dca_col + clearing_forwarding_col
      
            pivot_df[tax_cols] = pivot_df[tax_cols].fillna(0).astype(float)

            pivot_df['cgst_amt'] = pivot_df[cgst_col].sum(axis=1) if cgst_col else 0
            pivot_df['sgst_amt'] = pivot_df[sgst_col].sum(axis=1) if sgst_col else 0
            pivot_df['igst_amt'] = pivot_df[igst_col].sum(axis=1) if igst_col else 0

            if 'freight_amt' not in pivot_df.columns:
                pivot_df['freight_amt'] = 0.0

            if 'dca_amt' not in pivot_df.columns:
                pivot_df['dca_amt'] = 0.0

            if 'cf_amt' not in pivot_df.columns:
                pivot_df['cf_amt'] = 0.0

            pivot_df['freight_amt'] = pivot_df[freight_col].sum(axis=1) if freight_col else 0.0
            
            pivot_df['dca_amt'] = pivot_df[dca_col].sum(axis=1) if dca_col else 0.0
            pivot_df['cf_amt'] = pivot_df[clearing_forwarding_col].sum(axis=1) if clearing_forwarding_col else 0.0

            exclude_cols = set(merge_col + tax_cols + ['cgst_amt', 'sgst_amt', 'igst_amt','freight_amt','dca_amt','cf_amt','currency'])

            other_charge_cols = [col for col in pivot_df.columns if col not in exclude_cols and pd.api.types.is_numeric_dtype(pivot_df[col])]
            pivot_df['other_amt'] = pivot_df[other_charge_cols].sum(axis=1) if other_charge_cols else 0.0

            keep_col = merge_col + ['cgst_amt', 'sgst_amt', 'igst_amt',  'other_amt','freight_amt','dca_amt','cf_amt','currency']
            pivot_df = pivot_df[keep_col]
            
            df = pd.merge(left=df, right=pivot_df, how='right', on=merge_col)
            df_final = df
            
        else:
            df_final = df.copy()
            df_final['currency'] = "Unknown"
            req = ['cgst_amt', 'sgst_amt', 'igst_amt',  'other_amt','freight_amt','dca_amt','cf_amt','amount']
            for i in req:
                if i not in df_final.columns:
                    df_final[i] = 0.0

        item_col = ['Amount','QTY','Rate',"Discount"]
        for col in item_col:
            if col not in df_final.columns:
                df_final[col] = 0.0

        if 'Item Name' not in df_final.columns:
            df_final['Item Name'] = "No Item"

        if 'UOM' not in df_final.columns:
            df_final['UOM'] = "No Item"

        # Clean and fill missing tax fields
        cgst_col = [col for col in df_final.columns if col.lower().startswith('cgst output')]
        sgst_col = [col for col in df_final.columns if col.lower().startswith('sgst output')]
        igst_col = [col for col in df_final.columns if col.lower().startswith('igst output')]

        freight_col = [col for col in df_final.columns if col.lower().startswith('freight')]
        dca_col = [col for col in df_final.columns if col.lower().startswith("dca")]
        clearing_forwarding_col = [col for col in df_final.columns if col.lower().startswith("clearing & forwarding")]

        tax_cols = cgst_col + sgst_col + igst_col + freight_col + dca_col + clearing_forwarding_col

        df_final[tax_cols] = df_final[tax_cols].fillna(0).astype(float)
        df_final['cgst_amt'] = df_final[cgst_col].sum(axis=1) if cgst_col else df_final.get('cgst_amt', 0.0)
        df_final['sgst_amt'] = df_final[sgst_col].sum(axis=1) if sgst_col else df_final.get('sgst_amt', 0.0)
        df_final['igst_amt'] = df_final[igst_col].sum(axis=1) if igst_col else df_final.get('igst_amt', 0.0)

        df_final['freight_amt'] = df_final[freight_col].sum(axis=1) if freight_col else df_final.get('freight_amt', 0.0)
        df_final['dca_amt'] = df_final[dca_col].sum(axis=1) if dca_col else df_final.get('dca_amt', 0.0)
        df_final['cf_amt'] = df_final[clearing_forwarding_col].sum(axis=1) if clearing_forwarding_col else df_final.get('cf_amt', 0.0)

        # # # Normalize column names and rename
        df_final.columns = df_final.columns.str.lower().str.replace(" ", "_")
        cols_rename = {
            'voucher_date': 'date',
            'voucher_number': 'voucher_no',
            'party_name': 'particulars',
            'item_name': 'item',
            'uom': 'unit'
        }
        df_final = df_final.rename(columns=cols_rename)
        
        # # # Format date
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            df_final['date'] = pd.to_datetime(df_final['date'], dayfirst=True, errors='coerce').dt.date

        if 'bill_ref_no' not in df_final.columns:
            df_final['bill_ref_no'] = "Blank"
        else:
            df_final['bill_ref_no'] = df_final['bill_ref_no'].fillna("Blank")

        df_final['material_centre'] = material_centre_name

        df_final['extracted_symbol'] = df_final['amount'].astype(str).str.extract(r'(AU\$|CAD|£|€|\$)', expand=False)
        df_final['mapped_currency'] = df_final['extracted_symbol'].map(symbol_to_currency)
        
        df_final.loc[(df_final['currency'] == 'Unknown') & (df_final['mapped_currency'].notnull()), 'currency'] = df_final['mapped_currency']
        df_final.drop(columns=['extracted_symbol', 'mapped_currency'], inplace=True)
        
        df_final['amount'] = df_final['amount'].replace(r'[^\d.]', '', regex=True)
        df_final['amount'] = pd.to_numeric(df_final['amount'], errors='coerce')

        df_final['currency'] = df_final['currency'].str.replace('Unknown', "").replace("", np.nan)

        df_final['currency'] = np.where(df_final['currency'].isnull(), df_final['material_centre'].map(curr), df_final['currency'])
        
        df_final['fcy'] = np.where(df_final['material_centre'].isin(fcy_comp), 'Yes', 'No')
        df_final['rate'] = df_final['amount'] / df_final['qty']

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

        group_keys = ['date', 'voucher_no', 'particulars']

        df_final['other_amt'] = df_final.sort_values(by=['voucher_no', 'item']).groupby(group_keys)['other_amt'].transform(lambda x: [x.iloc[0]] + [0] * (len(x) - 1))
        df_final['freight_amt'] = df_final.sort_values(by=['voucher_no', 'item']).groupby(group_keys)['freight_amt'].transform(lambda x: [x.iloc[0]] + [0] * (len(x) - 1))
        df_final['dca_amt'] = df_final.sort_values(by=['voucher_no', 'item']).groupby(group_keys)['dca_amt'].transform(lambda x: [x.iloc[0]] + [0] * (len(x) - 1))
        df_final['cf_amt'] = df_final.sort_values(by=['voucher_no', 'item']).groupby(group_keys)['cf_amt'].transform(lambda x: [x.iloc[0]] + [0] * (len(x) - 1))

        voucher_totals = df_final.groupby(group_keys)[['amount', 'cgst_amt', 'sgst_amt', 'igst_amt', 'other_amt','freight_amt','dca_amt','cf_amt']].sum()
        voucher_totals['total_amt'] = voucher_totals.sum(axis=1)
        voucher_totals = voucher_totals[['total_amt']].reset_index()
        
        df_final = df_final.merge(voucher_totals, on=group_keys, how='left')
        df_final = df_final.sort_values(by=['voucher_no', 'item'])
        df_final['total_amt'] = df_final.groupby(group_keys)['total_amt'].transform(lambda x: [x.iloc[0]] + [0] * (len(x) - 1))

        final_columns = [
            'date', 'voucher_no', 'bill_ref_no', 'voucher_type', 'particulars', 'item', 'qty', 'unit',
            'rate', 'amount', 'discount', 'cgst_amt', 'sgst_amt', 'igst_amt','freight_amt','dca_amt','cf_amt', 'other_amt', 'total_amt',
            'material_centre', 'currency', 'fcy', 'narration'
        ]

        for col in final_columns:
            if col not in df_final.columns:
                df_final[col] = None

        df_final = df_final[final_columns]

        return df_final

    except Exception as e:
        print(f"A processing error occurred: {e}")
    finally:
        print("Script completed.")


if __name__ =="__main__":
    p1 = r"D:\User Profile\Desktop\api_download\Thane KBEIPL\Bulk_Export Credit Note_24_5_2025_18_08_50_.json"
    p2 = r"D:\User Profile\Desktop\api_download\FCY Freshnova\Bulk_Credit Note_24_5_2025_18_14_02_.json"
    p3 = r"E:\api_download\FCY Frexotic\Bulk_Credit Note_26_5_2025_14_42_14_.json"
    APISalesReturnVoucher(p3,'Thane KBEIPL')


