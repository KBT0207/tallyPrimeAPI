import glob
import pandas as pd
import os
from datetime import datetime, timedelta
from database.sql_connector import kbbio_engine, kbbio_connector, kbe_connector, kbe_engine
from database.busy_data_processor import BusyDataProcessor, get_filename, get_compname
from database.tally_data_processor import get_compname_tally,get_date_tally,get_filename_tally
from database.tally_data_processor import TallyDataProcessor
from database.models.base import KBBIOBase, KBEBase
from database.db_crud import DatabaseCrud
from logging_config import logger
from utils.common_utils import busy_tables, tally_tables , busyrm_tables
from utils.email import email_send
from main_reports.reports import Reports
from database.tally_data_processor import get_exchange_rate_in_inr
import requests



def truncate_busy_masters():    
    KBBIOBase.metadata.create_all(kbbio_engine)    

    tables_list = list(busyrm_tables.keys())
    importer = DatabaseCrud(kbbio_connector)
    for table in tables_list:
        if "acc" in table or "items" in table:
            importer.truncate_table(table_name=table, commit=True)
    
def delete_busy_sales(startdate:str, enddate:str, commit:bool):   
    if startdate <= enddate:
        KBBIOBase.metadata.create_all(kbbio_engine)

        busy_sales_table = ['busy_sales', 'busy_sales_order', 'busy_sales_return']
        importer = DatabaseCrud(kbbio_connector)
        for table in busy_sales_table:
            importer.delete_date_range_query(table, start_date= startdate, end_date=enddate, commit=commit)
    else:
        logger.critical(f"Start date: {startdate} should be equal or greater than end date: {enddate}.")

def delete_busy_purchase(startdate:str, enddate:str, commit:bool):   
    if startdate <= enddate:
        KBBIOBase.metadata.create_all(kbbio_engine)

        busyrm_purchase_table = ['busyrm_purchase', 'busyrm_purchase_order','busyrm_purchase_return']
        importer = DatabaseCrud(kbbio_connector)
        for table in busyrm_purchase_table:
            importer.delete_date_range_query(table, start_date= startdate, end_date=enddate, commit=commit)
    else:
        logger.critical(f"Start date: {startdate} should be equal or greater than end date: {enddate}.")

def delete_busy_stock(startdate:str, enddate:str, commit:bool):   
    if startdate <= enddate:
        KBBIOBase.metadata.create_all(kbbio_engine)

        busyrm_purchase_table = ['busyrm_stock_transfer', 'busyrm_stock_journal', 'busyrm_production']
        importer = DatabaseCrud(kbbio_connector)
        for table in busyrm_purchase_table:
            importer.delete_date_range_query(table, start_date= startdate, end_date=enddate, commit=commit)
    else:
        logger.critical(f"Start date: {startdate} should be equal or greater than end date: {enddate}.")

def delete_busy_material(from_date: str, to_date: str):    
    KBBIOBase.metadata.create_all(kbbio_engine)

    tables_list = ["busyrm_mrfp", "busyrm_mitp"]
    importer = DatabaseCrud(kbbio_connector)

    for table in tables_list:
        importer.delete_date_range_query(table, start_date=from_date, end_date=to_date, commit=True)

def delete_tally_data(start_date:str, end_date:str, file_date:str, commit:bool): 
    
    KBEBase.metadata.create_all(kbe_engine)
    tally_files = glob.glob("E:\\automated_tally_downloads\\" + f"**\\*{file_date}.xlsx", recursive=True)
    material_centre_set = set()
    if len(tally_files) != 0:
        for file in tally_files:
            mc = get_compname_tally(file).replace("_", " ")
            mc = mc.replace("_", " ")
            material_centre_set.add(mc)
        
        delete_tally_data_mc_wise = DatabaseCrud(kbe_connector)
    tables_list = list(tally_tables.keys())
    
    exclude_tables = ['tally_accounts', 'outstanding_balance', 'tally_receivables','exchange_rate']
    for table in tables_list:
        if table not in exclude_tables:
            delete_tally_data_mc_wise.delete_tally_material_centre_and_datewise(table, 
                                            start_date= start_date, end_date=end_date, 
                                            commit=commit, material_centre=material_centre_set)
    # importer.truncate_table(table_name= 'tally_accounts', commit= commit)

def import_busy_sales(filename:str):
    KBBIOBase.metadata.create_all(kbbio_engine)
    
    busy_files = glob.glob("E:\\automated_busy_downloads\\" + f"**\\*sales*{filename}.xlsx", recursive=True)
    if len(busy_files) != 0:
        for file in busy_files:
            excel_data = BusyDataProcessor(file)
            importer = DatabaseCrud(kbbio_connector)
            if get_filename(file) == 'sales':
                importer.import_data('busy_sales', excel_data.clean_and_transform(), commit=True)
    
            if get_filename(file) == 'sales_return':
                importer.import_data('busy_sales_return', excel_data.clean_and_transform(), commit=True)

            if get_filename(file) == 'sales_order':
                importer.import_data('busy_sales_order', excel_data.clean_and_transform(), commit=True)

            else:
                logger.error(f"{get_filename(file)} and {get_compname(file)} of {file} didn't match the criteria")    

    else:
        logger.critical("No File for today's date found to import in database")        

def import_busyrm_purchase(filename:str):
    KBBIOBase.metadata.create_all(kbbio_engine)
    
    busy_files = glob.glob("E:\\automated_busy_downloads\\" + f"**\\*purchase*{filename}.xlsx", recursive=True)
    if len(busy_files) != 0:
        for file in busy_files:
            excel_data = BusyDataProcessor(file)
            importer = DatabaseCrud(kbbio_connector)
            if get_filename(file) == 'purchase':
                importer.import_data('busyrm_purchase', excel_data.clean_and_transform(), commit=True)
    
            if get_filename(file) == 'purchase_return':
                importer.import_data('busyrm_purchase_return', excel_data.clean_and_transform(), commit=True)

            if get_filename(file) == 'purchase_order':
                importer.import_data('busyrm_purchase_order', excel_data.clean_and_transform(), commit=True)

            else:
                logger.error(f"{get_filename(file)} and {get_compname(file)} of {file} didn't match the criteria")    

    else:
        logger.critical("No File for today's date found to import in database") 

def import_busy_purchase(filename:str):    
    KBBIOBase.metadata.create_all(kbbio_engine)
        
    busy_files = glob.glob("E:\\automated_busy_downloads\\" + f"**\\*purchase*{filename}.xlsx", recursive=True)
    if len(busy_files) != 0:
        for file in busy_files:
            excel_data = BusyDataProcessor(file)
            importer = DatabaseCrud(kbbio_connector)
            if get_filename(file) == 'purchase':
                importer.import_data('busy_purchase', excel_data.clean_and_transform(), commit=True)
    
            if get_filename(file) == 'purchase_return':
                importer.import_data('busy_purchase_return', excel_data.clean_and_transform(), commit=True)

            else:
                logger.error(f"{get_filename(file)} and {get_compname(file)} of {file} didn't match the criteria")    

    else:
        logger.critical("No File for today's date found to import in database")        

def import_busy_masters_material(file_name:str):
    KBBIOBase.metadata.create_all(kbbio_engine)
    # today_date = "17-Apr-2024"

    pattern_master = f"E:\\automated_busy_downloads\\**\\*master*{file_name}.xlsx"
    pattern_item = f"E:\\automated_busy_downloads\\**\\*items*{file_name}.xlsx"
    pattern_material = f"E:\\automated_busy_downloads\\**\\*material*{file_name}.xlsx"

    busy_files_material = glob.glob(pattern_material, recursive=True)
    busy_files_master = glob.glob(pattern_master, recursive=True)
    busy_files_item = glob.glob(pattern_item, recursive=True)

    busy_files = busy_files_master + busy_files_item + busy_files_material
    if len(busy_files) != 0:
        for file in busy_files:
            excel_data = BusyDataProcessor(file)
            importer = DatabaseCrud(kbbio_connector)

            if get_filename(file) == 'material_issued_to_party':
                importer.import_data('busyrm_mitp', excel_data.clean_and_transform(), commit=True)
                
            if get_filename(file) == 'material_received_from_party':
                importer.import_data('busyrm_mrfp', excel_data.clean_and_transform(), commit=True)


            if get_filename(file) == "master_accounts" and get_compname(file) == "comp0003":
                importer.import_data('busyrm_acc', excel_data.clean_and_transform(), commit=True)

            if get_filename(file) == "items" and get_compname(file) == "comp0003":
                importer.import_data('busyrm_items', excel_data.clean_and_transform(), commit=True)

    else:
        logger.critical("No File for today's date found to import in database")

def import_tally_data(date):
    KBEBase.metadata.create_all(kbe_engine)
    
    tally_files = glob.glob("E:\\automated_tally_downloads\\" + f"**\\*{date}.xlsx", recursive=True)
    if len(tally_files) != 0:
        for file in tally_files:
            excel_data = TallyDataProcessor(file)
            importer = DatabaseCrud(kbe_connector)
            if get_filename_tally(file) == 'sales':
                importer.import_data('tally_sales', excel_data.clean_and_transform(), commit=True)
    
            if get_filename_tally(file) == 'sales-return':
                importer.import_data('tally_sales_return', excel_data.clean_and_transform(), commit=True)

            if get_filename_tally(file) == 'purchase':
                importer.import_data('tally_purchase', excel_data.clean_and_transform(), commit=True)
    
            if get_filename_tally(file) == 'purchase-return':
                importer.import_data('tally_purchase_return', excel_data.clean_and_transform(), commit=True)
            
            if get_filename_tally(file) == 'payments':
                importer.import_data('tally_payments', excel_data.clean_and_transform(), commit=True)

            if get_filename_tally(file) == 'receipts':
                importer.import_data('tally_receipts', excel_data.clean_and_transform(), commit=True)

            if get_filename_tally(file) == 'journal':
                importer.import_data('tally_journal', excel_data.clean_and_transform(), commit=True)
                
            if get_filename_tally(file) == 'sales-detailed':
                importer.import_data("tally_sales_detailed",excel_data.clean_and_transform(),commit=True)

            if get_filename_tally(file) == 'sales-return-detailed':
                importer.import_data("tally_sales_return_detailed",excel_data.clean_and_transform(),commit=True)
                
                        
            # if get_compname_tally(file) == 'sales-return-detailed':
            #     importer.import_data("tally_sales_details",excel_data.clean_and_transform(),commit=True)

            # if get_filename_tally(file) == 'accounts':
            #     importer.import_accounts_data(df=excel_data.clean_and_transform(), commit=True)

            # if get_filename_tally(file) == 'items':
            #     importer.import_data('tally_items', excel_data.clean_and_transform(), commit=True)

                logger.info(f"{get_filename_tally(file)} and {get_compname(file)} imported into database.. ")

    else:
        logger.critical("No File for today's date found to import in database")

def import_outstanding_tallydata(dates: list, monthly: bool):
    KBEBase.metadata.create_all(kbe_engine)

    for date in dates:
        if monthly:
            first_day_of_current_month = datetime.today().replace(day=1)
            previous_month = (first_day_of_current_month - timedelta(days=1)).strftime('%B-%Y')    
             
            tally_files = glob.glob(f"E:\\monthly_data\\**\\{previous_month}" + f"**\\*outstanding_{date}.xlsx",  recursive=True)
        else:
            tally_files = glob.glob(rf"E:\automated_tally_downloads\**\*outstanding_{date}.xlsx", recursive= True)
        
        # Using glob to search recursively
        if tally_files:  # Same as checking if len(tally_files) != 0
            for file in tally_files:
                excel_data = TallyDataProcessor(file)
                importer = DatabaseCrud(kbbio_connector)
                if get_filename_tally(file) == 'outstanding':
                    importer.import_data('outstanding_balance', excel_data.clean_and_transform(), commit=True)



# def import_kbe_outstanding_tallydata(dates: list):
#     KBEBase.metadata.create_all(kbe_engine)

#     for date in dates:
#         tally_files = glob.glob(rf"D:\automated_kbe_downloads\**\*kbe_outstanding_{date}.xlsx", recursive= True)
        
#         # Using glob to search recursively
#         if tally_files: 
#             for file in tally_files:
#                 excel_data = TallyDataProcessor(file)
#                 importer = DatabaseCrud(kbe_connector)
#                 if get_filename(file) == 'kbe_outstanding':
#                     importer.import_data('outstanding_balance', excel_data.clean_and_transform(), commit=True)
#         else:
#             print("No KBE Outstanding Files")



def import_receivables_tallydata(dates: list, monthly: bool):    
    KBEBase.metadata.create_all(kbe_engine)
    for date in dates:
        if monthly:
            first_day_of_current_month = datetime.today().replace(day=1)
            previous_month = (first_day_of_current_month - timedelta(days=1)).strftime('%B-%Y')
            
            tally_files = glob.glob(f"E:\\monthly_data\\**\\{previous_month}" + f"**\\*receivables_{date}.xlsx",  recursive=True)
        else:
            tally_files = glob.glob(rf"D:\automated_tally_downloads\**\*receivables_{date}.xlsx", recursive= True)
        if tally_files:
            for file in tally_files:
                excel_data = TallyDataProcessor(file)
                importer = DatabaseCrud(kbbio_connector)
                if get_filename_tally(file) == 'receivables':
                    importer.import_data('tally_receivables', excel_data.clean_and_transform(), commit=True)

def import_busy_stock(filename:str):    
    KBBIOBase.metadata.create_all(kbbio_engine)
        
    busy_files = glob.glob("E:\\automated_busy_downloads\\" + f"**\\*stock_transfer_{filename}.xlsx", recursive=True) + \
                 glob.glob("E:\\automated_busy_downloads\\" + f"**\\*production_{filename}.xlsx", recursive=True) + \
                 glob.glob("E:\\automated_busy_downloads\\" + f"**\\*stock_journal_{filename}.xlsx", recursive=True)
    
    if len(busy_files) != 0:
        for file in busy_files:
            excel_data = BusyDataProcessor(file)
            importer = DatabaseCrud(kbbio_connector)
            if get_filename(file) == 'stock_transfer':
                importer.import_data('busyrm_stock_transfer', excel_data.clean_and_transform(), commit=True)
    
            if get_filename(file) == 'stock_journal':
                importer.import_data('busyrm_stock_journal', excel_data.clean_and_transform(), commit=True)

            if get_filename(file) == 'production':
                importer.import_data('busyrm_production', excel_data.clean_and_transform(), commit=True)

            else:
                logger.error(f"{get_filename(file)} and {get_compname(file)} of {file} didn't match the criteria")    

    else:
        logger.critical("No File for today's date found to import in database")

def dealer_price_validation_report(from_date:str, to_date:str, effective_date:str, send_email:bool, exceptions:list = None) -> None:
    """Generated dealer price validation report as per the arguments.

    Args:
        from_date (str): The date from which busy sales needed to be validated from.
        to_date (str): The date till which busy sales needed to be validated.
        send_email (bool): when False only excel file with report get generated. True if you want to send email with the excel file.
        exceptions (list, optional): Takes in Sales Voucher Number which you want to be excluded from the report. Defaults to None.
    """
    reports = Reports(kbbio_connector)
    
    validation_df = reports.sales_price_validation(from_date= from_date, to_date= to_date, 
                                                   effective_date= effective_date, exceptions= exceptions)
    
    counts = len(validation_df)
    if counts != 0:
        
        validation_df.to_excel(fr"D:\Reports\Busy_Sales_Price\Price Validation from Month to {to_date}.xlsx", index= False)
        
        subject = f"Busy Sales Price Validation Report from Month to {to_date} with {counts} rows of discrepancies"
        body = f"Greetings All,\nKindly find the Busy Sales Price Validation Report attached from Month to {to_date} with {counts} rows of discrepancies.\n In the attached excel, column 'Total Price' is the sum of List Price ('Sales_Price') and 'Discout_Amt' which is the compared with the actual Price List."
        attachment = fr"D:\Reports\Busy_Sales_Price\Price Validation from Month to {to_date}.xlsx"
        logger.info(f"Busy Sales Price Validation Report Exported to Excel with {counts} Discrepencies")

    else:
        subject = f"Busy Sales Price Validation Report from Month to {to_date} without discrepancy"
        attachment = None
        body = f"Greetings All,\nAs per yesterday's data, there were no discrepancy found in busy sales with the price list."

        logger.info(f"Busy Sales Price Validation Report Produced without discrepancies")

    if send_email:
        try:
            receivers = ['shivprasad@kaybeebio.com', 
                        'holkar.h@kaybeebio.com'
                        ]
            cc = ['danish@kaybeeexports.com', 's.gaurav@kaybeeexports.com', 
                'mahendra@kaybeeexports.com'
                ]
            email_send(reciever= receivers, 
                       cc= cc, 
                       subject= subject, contents= body, attachemnts= attachment)
            logger.info(f"Successfully emailed the Busy Sales Price Validation Report.")
        except Exception as e:
            logger.critical(f"Failed to email the Busy Sales Price Validation Report : {e}")

def salesorder_salesman_report(from_date:str, to_date:str, send_email:bool, exceptions:list = None) -> None:
    reports = Reports(kbbio_connector)
    
    validation_df = reports.salesman_order_validation(from_date= from_date, to_date= to_date, exceptions= exceptions)
    
    counts = len(validation_df)
    if counts != 0:
        
        validation_df.to_excel(fr"D:\Reports\Busy_SalesOrder_Salesman\Salesman Validation from Month to {to_date}.xlsx", index= False)
        
        subject = f"Busy SalesOrder Salesman Validation Report from Month to {to_date} with {counts} rows of discrepancies"
        body = f"Greetings All,\nKindly find the Busy SalesOrder Salesman Validation Report attached from Month to {to_date} with {counts} rows of discrepancies.\nThe attached excel contains the busy entries without the mention of salesman name."
        attachment = fr"D:\Reports\Busy_SalesOrder_Salesman\Salesman Validation from Month to {to_date}.xlsx"
        logger.info(f"Busy SalesOrder Salesman Validation Report Exported to Excel with {counts} Discrepencies")

    else:
        subject = f"Busy SalesOrder Salesman Validation Report from Month to {to_date} without discrepancy"
        attachment = None
        body = f"Greetings All,\nAs per yesterday's data, there were no descrepancy found in busy salesorder regarding salesman."

        logger.info(f"SalesOrder Salesman Validation Report Produced without discrepancies")

    if send_email:
        try:
            receivers = ['shivprasad@kaybeebio.com', 
                        ]
            cc = ['danish@kaybeeexports.com', 's.gaurav@kaybeeexports.com', 
                ]
            email_send(reciever= receivers, 
                       cc= cc, 
                       subject= subject, contents= body, attachemnts= attachment)
            logger.info(f"Successfully emailed the Busy SalesOrder Salesman Validation Report.")
        except Exception as e:
            logger.critical(f"Failed to email the Busy SalesOrder Salesman Validation Report : {e}")

def volume_discount_report(dates:list, send_email:bool, exceptions:list = None) -> None:
    
    def filename_date(date_range= dates) -> str:
        if len(dates) > 1:
            name = f'from {date_range[0]} to {date_range[-1]}'
        else:
            name = f'of {date_range[0]}'
        return name
    
    reports = Reports(kbbio_connector)
    
    validation_df = reports.volume_discount_validation(dates= dates, exceptions= exceptions)
    # return view(validation_df)
    validation_df.to_excel(fr"D:\Reports\Volume_Discount\Volume Discount Report {filename_date(date_range=dates)}.xlsx", index= False)
    
    discrepancy_count = validation_df.loc[validation_df['remark'] == 'Discrepancy', 'remark'].count() 
    # print(discrepancy_count)
    if discrepancy_count > 0:
        subject = f"Busy Sales Volume Discount Report {filename_date(date_range=dates)} with {discrepancy_count} discrepancies"
        body = f"Greetings All,\nKindly find the Busy Sales Volume Discount Report {filename_date(date_range=dates)} attached with discrepancy."
        logger.info(f"Busy Sales Volume Discount Report Exported to Excel with {discrepancy_count} Discrepencies")

    else:
        subject = f"Busy Sales Volume Discount Report {filename_date(date_range=dates)} without discrepancy"
        body = f"Greetings All,\nAs per the data, there were no descrepancy found in busy sales regarding volume discount."
        logger.info(f"Volume Discount Report Produced without discrepancies")

    if send_email:
        attachment = fr"D:\Reports\Volume_Discount\Volume Discount Report {filename_date(date_range=dates)}.xlsx"
        try:
            receivers = ['shivprasad@kaybeebio.com', 
                        ]
            cc = ['danish@kaybeeexports.com', 's.gaurav@kaybeeexports.com', 
                ]
            email_send(reciever= receivers, 
                       cc= cc, 
                       subject= subject, contents= body, attachemnts= attachment)
            logger.info(f"Successfully emailed the Busy Sales Volume Discount Report.")
        except Exception as e:
            logger.critical(f"Failed to email the Busy Sales Volume Discount Report : {e}")

def cash_discount_report(dates:list, send_email:bool, exceptions:list = None) -> None:

    def filename_date(date_range= dates) -> str:
        if len(dates) > 1:
            name = f'from {date_range[0]} to {date_range[-1]}'
        else:
            name = f'of {date_range[0]}'
        return name
    
    reports = Reports(kbbio_connector)
    # from xlwings import view
    validation_df = reports.cash_discount_validation(dates= dates, exceptions= exceptions)
    # return print(validation_df)
    validation_df.to_excel(fr"D:\Reports\Cash_Discount\Cash Discount Report {filename_date(date_range= dates)}.xlsx", index= False)
    
    discrepancy_count = validation_df.loc[validation_df['remark'] == 'Discrepancy', 'remark'].count() 
    if discrepancy_count > 0:
        subject = f"Busy Sales Cash Discount Report {filename_date(date_range= dates)} with {discrepancy_count} discrepancies"
        body = f"Greetings All,\nKindly find the Busy Sales Cash Discount Report {filename_date(date_range= dates)} attached with discrepancy."
        logger.info(f"Busy Sales Cash Discount Report Exported to Excel with {discrepancy_count} Discrepencies")

    else:
        subject = f"Busy Sales Cash Discount Report {filename_date(date_range= dates)} without discrepancy"
        body = f"Greetings All,\nAs per the data of the above mentioned dates, there were no descrepancy found in busy sales regarding Cash discount."
        logger.info(f"Cash Discount Report Produced without discrepancies")

    if send_email:
        attachment = fr"D:\Reports\Cash_Discount\Cash Discount Report {filename_date(date_range= dates)}.xlsx"
        try:
            receivers = ['shivprasad@kaybeebio.com', 
                        ]
            cc = ['danish@kaybeeexports.com', 's.gaurav@kaybeeexports.com', 
                ]
            email_send(reciever= receivers, 
                       cc= cc, 
                       subject= subject, contents= body, attachemnts= attachment)
            logger.info(f"Successfully emailed the Busy Sales Cash Discount Report.")
        except Exception as e:
            logger.critical(f"Failed to email the Busy Sales Cash Discount Report : {e}")

def busy_tally_sales_reco(start_date:str, end_date:str, send_email:bool, exceptions:list = None) -> None:
    report = Reports(kbbio_connector)
    try:
        report_file_path = report.sales_validation(fromdate= start_date, todate= end_date, exceptions= exceptions)
        logger.info(f"Busy-Tally sales reco of previous week exported in excel")
        busy_sales_df = pd.read_excel(report_file_path, sheet_name= 'Busy Sales')
        tally_sales_df = pd.read_excel(report_file_path, sheet_name= 'Tally Sales')
    except Exception as e :
        logger.critical(f"Error occured: {e} \n\nWhile exporting Busy-Tally sales reco from {start_date} to {end_date} in excel format")
    busy_amnt_discrepancy = busy_sales_df.loc[busy_sales_df['amount_diff'] >= 5].shape[0]
    tally_amnt_discrepancy = tally_sales_df.loc[tally_sales_df['amount_diff'] >= 5].shape[0]
    busy_gst_discrepancy = busy_sales_df.loc[busy_sales_df['gst_remark'] == 'Matched'].shape[0]
    tally_gst_discrepancy = tally_sales_df.loc[tally_sales_df['gst_remark'] == 'Matched'].shape[0]

    if (busy_amnt_discrepancy > 0) or (tally_amnt_discrepancy > 0) or (busy_gst_discrepancy > 0) or (tally_gst_discrepancy > 0):
        subject = f"Discrepancy found in Busy-Tally Sales Reco from {start_date} to {end_date}"
        body = f"Greetings All,\nKindly find the Busy-Tally Sales Reco from {start_date} to {end_date} attached with discrepancies."
        logger.info(f"Busy-Tally Sales Reco Exported to Excel with discrepancy.")

    else:
        subject = f"No discrepancy found in Busy-Tally Sales Reco from {start_date} to {end_date}"
        body = f"Greetings All,\nKindly find the Busy-Tally Sales Reco from {start_date} to {end_date} attached without discrepancies."
        logger.info(f"Busy-Tally Sales Reco Exported to Excel without discrepancy.")

    if send_email:
        attachment = report_file_path
        try:
            receivers = ['shivprasad@kaybeebio.com', 
                        ]
            cc = ['danish@kaybeeexports.com', 's.gaurav@kaybeeexports.com', 
                ]
            email_send(reciever= receivers, 
                       cc= cc, 
                       subject= subject, contents= body, attachemnts= attachment)
            logger.info(f"Successfully emailed the Busy-Tally Sales Reco Report.")
        except Exception as e:
            logger.critical(f"Failed to email the Busy-Tally Sales Reco Report: {e}")

def busy_tally_salesreturn_reco(start_date:str, end_date:str, send_email:bool, exceptions:list = None) -> None:
    report = Reports(kbbio_connector)
    try:
        report_file_path = report.sales_return_validation(fromdate= start_date, todate= end_date, exceptions= exceptions)
        logger.info(f"Busy-Tally sales return reco from {start_date} to {end_date} exported in excel")
        busy_df = pd.read_excel(report_file_path, sheet_name= 'Busy Sales Return')
        tally_df = pd.read_excel(report_file_path, sheet_name= 'Tally Sales Return')
    except Exception as e :
        logger.critical(f"Error occured: {e} \n\nWhile exporting Busy-Tally sales return reco from {start_date} to {end_date} in excel format")
    busy_amnt_discrepancy = busy_df.loc[busy_df['amount_diff'] >= 5].shape[0]
    tally_amnt_discrepancy = tally_df.loc[tally_df['amount_diff'] >= 5].shape[0]
    busy_gst_discrepancy = busy_df.loc[busy_df['gst_remark'] == 'Matched'].shape[0]
    tally_gst_discrepancy = tally_df.loc[tally_df['gst_remark'] == 'Matched'].shape[0]

    if (busy_amnt_discrepancy > 0) or (tally_amnt_discrepancy > 0) or (busy_gst_discrepancy > 0) or (tally_gst_discrepancy > 0):
        subject = f"Discrepancy found in Busy-Tally Sales Return Reco from {start_date} to {end_date}"
        body = f"Greetings All,\nKindly find the Busy-Tally Sales Return Reco from {start_date} to {end_date} attached with discrepancies."
        logger.info(f"Busy-Tally Sales Return Reco Exported to Excel with discrepancy.")

    else:
        subject = f"No discrepancy found in Busy-Tally Sales Return Reco from {start_date} to {end_date}"
        body = f"Greetings All,\nKindly find the Busy-Tally Sales Return Reco from {start_date} to {end_date} attached without discrepancies."
        logger.info(f"Busy-Tally Sales Return Reco Exported to Excel without discrepancy.")

    if send_email:
        attachment = report_file_path
        try:
            receivers = ['shivprasad@kaybeebio.com', 
                        ]
            cc = ['danish@kaybeeexports.com', 's.gaurav@kaybeeexports.com', 
                ]
            email_send(reciever= receivers, 
                       cc= cc, 
                       subject= subject, contents= body, attachemnts= attachment)
            logger.info(f"Successfully emailed the Busy-Tally Sales Return Reco Report.")
        except Exception as e:
            logger.critical(f"Failed to email the Busy-Tally Sales Return Reco Report: {e}")

def salesorder_mitp_reco_report(start_date:str, end_date:str, send_email:bool, exceptions:list = None) -> None:
    reports = Reports(kbbio_connector)
    salesorder_df = reports.salesorder_mitp_reco(fromdate= start_date, todate= end_date, exceptions= exceptions)
    salesorder_df.to_excel(fr"D:\Reports\SalesOrder_MITP_Reco\SalesOrder-MITP-Reco-Month-to-{end_date}.xlsx", index= False)
    
    discrepancy_count = salesorder_df.loc[salesorder_df['remark'] == 'Discrepancy', 'remark'].count() 
    if discrepancy_count > 0:
        subject = f"Busy Sales Order-MITP Reco from Month to {end_date} with {discrepancy_count} discrepancies"
        body = f"Greetings All,\nKindly find the Busy Sales Order - MITP Reco from Month to {end_date} attached with discrepancy."
        logger.info(f"Busy Sales Order - MITP Reco Exported to Excel with {discrepancy_count} Discrepencies")
    
    else:
        subject: f"Busy Sales Order-MITP Reco from Month to {end_date} without discrepancies"
        body = f"Greetings All,\nKindly find the Busy Sales Order - MITP Reco from Month to {end_date} attached without discrepancy."
        logger.info(f"Busy Sales Order - MITP Reco Exported to Excel without Discrepencies")

    if send_email:
        attachment = fr"D:\Reports\SalesOrder_MITP_Reco\SalesOrder-MITP-Reco-Month-to-{end_date}.xlsx"
        try:
            receivers = ['shivprasad@kaybeebio.com', 
                        ]
            cc = ['danish@kaybeeexports.com', 's.gaurav@kaybeeexports.com', 
                ]
            email_send(reciever= receivers, 
                       cc= cc, 
                       subject= subject, contents= body, attachemnts= attachment)
            logger.info(f"Successfully emailed the Busy Sales Order - MITP Reco.")
        except Exception as e:
            logger.critical(f"Failed to email the Busy Sales Order - MITP Reco : {e}")

def get_latest_date_from_api() -> str | None:
    """
    Fetch the latest available date from the exchange rate API using a sample currency.
    Returns the latest date as a string.
    """
    try:
        # Use a sample currency to get the latest date, e.g., "USD"
        api_url = "https://api.frankfurter.app/latest?base=USD&symbols=INR"
        response = requests.get(api_url)
        response.raise_for_status()
        latest_data = response.json()
        
        # Extract the date
        latest_date = latest_data.get("date")
        return latest_date

    except requests.RequestException as e:
        logger.error(f"Failed to fetch the latest date from API: {e}")
        return None


# def update_exchange_rate(dates: list):
#     currency_list = ['USD', 'EUR', 'GBP', 'CAD', 'AUD', 'HKD', 'THB', 'SGD', 'INR']
    
#     KBEBase.metadata.create_all(kbe_engine)
#     logger.info(f'Update exchange rate table for {dates}')
    
#     exchange_rate_records = []
    
#     # Retrieve the latest date from the API for INR entries
#     latest_date = get_latest_date_from_api()
#     if not latest_date:
#         logger.error("Failed to retrieve the latest date; cannot update exchange rates.")
#         return
    
#     for dte in dates:
#         for currency in currency_list:
#             if currency == 'INR':
#                 # Add INR record with rate 1 and the latest date from the API
#                 exchange_rate_records.append({
#                     "date": latest_date,
#                     "currency": "INR",
#                     "exchange_rate": 1
#                 })
#             else:
#                 # Fetch rate and date for other currencies
#                 rate_info = get_exchange_rate_in_inr(currency, dte)
#                 if rate_info:
#                     rate = rate_info.get("rate", 0)
#                     date_rate = rate_info.get("date")
                    
#                     exchange_rate_records.append({
#                         "date": date_rate,
#                         "currency": currency,
#                         "exchange_rate": rate
#                     })
    
#     if exchange_rate_records:
#         df_exchange_rates = pd.DataFrame(exchange_rate_records)
#         df_exchange_rates = df_exchange_rates.drop_duplicates(subset=['date', 'currency', 'exchange_rate'])
        
#         db_crud = DatabaseCrud(kbe_connector)
#         db_crud.delete_date_range_query(
#             table_name='exchange_rate', 
#             start_date=latest_date, 
#             end_date=latest_date, 
#             commit=True
#         )
        
#         db_crud.import_data(table_name='exchange_rate', df=df_exchange_rates, commit=True)
#         logger.info(f"Data imported for {set(df_exchange_rates['date'].to_list())}")



    



