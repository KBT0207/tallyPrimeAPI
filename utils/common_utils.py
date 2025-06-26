"""This module contain functions that will used as helper/common functions in the report modules 
"""
import calendar
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

import psutil

def is_process_running(process_name:str) -> bool:
    """This method will check whether a specific process is running or not.

    Args:
        process_name (_type_): Name of the process which you want to check it is running or not.

    Returns:
        _type_: Returns True if provided process_name is already running.
                Returns False if provided process_name is not running. 
    """
    for process in psutil.process_iter():
        if process.name().lower() == process_name.lower():
            return True
    return False




def get_specific_fiscal_quarter_date(q_number: int):
    today = datetime.today().date()
    month = today.month
    year = today.year

    # Determine current fiscal quarter and fiscal year
    if 4 <= month <= 6:
        current_q = 1
        fiscal_year = year
    elif 7 <= month <= 9:
        current_q = 2
        fiscal_year = year
    elif 10 <= month <= 12:
        current_q = 3
        fiscal_year = year
    else:  # Jan to Mar
        current_q = 4
        fiscal_year = year - 1

    # Backtrack to target quarter
    target_q = current_q
    target_year = fiscal_year
    for _ in range(q_number - 1):
        target_q -= 1
        if target_q == 0:
            target_q = 4
            target_year -= 1

    # Get quarter start and end dates
    if target_q == 1:
        start = datetime(target_year, 4, 1).date()
        end = datetime(target_year, 6, 30).date()
    elif target_q == 2:
        start = datetime(target_year, 7, 1).date()
        end = datetime(target_year, 9, 30).date()
    elif target_q == 3:
        start = datetime(target_year, 10, 1).date()
        end = datetime(target_year, 12, 31).date()
    else:  # Q4
        start = datetime(target_year + 1, 1, 1).date()
        end = datetime(target_year + 1, 3, 31).date()

    # If this is the current quarter, use today as the end date
    if target_q == current_q and target_year == fiscal_year:
        end = today

    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")




from database.models.kbe_models.tally_kbe_models import (TallySalesDetailed,TallyPurchaseDetailed, TallyPurchaseReturnDetailed,TallySalesReturnDetailed,
                                                         TallyMasters,TallyItems,TallyItemsMapping,TallyReceipt,TallyPayments,TallyJournal
                                                         )



def batch_date(month: int, batch: int, year: int = datetime.today().year) -> list:
    if batch not in [1, 2, 3]:
        raise ValueError("Batch number must be 1, 2, or 3")
    
    # Get the total number of days in the month
    days_in_month = calendar.monthrange(year, month)[1]
    
    # Calculate the size of each batch
    batch_size = days_in_month // 3
    remainder = days_in_month % 3

    # Determine the start and end dates for each batch
    if batch == 1:
        start_day = 1
        end_day = batch_size
    elif batch == 2:
        start_day = batch_size + 1
        end_day = 2 * batch_size
    else:  # batch == 3
        start_day = 2 * batch_size + 1
        end_day = days_in_month
    
    # If there's a remainder, adjust the batches
    if remainder > 0:
        if batch == 1:
            end_day += 1
        elif batch == 2:
            start_day += 1
            end_day += 1
        else:  # batch == 3
            start_day += 2
    
    # Generate the list of dates for the batch
    return [f"{day:02d}-{month:02d}-{year}" for day in range(start_day, end_day + 1)]



tally_tables = { 
                "tally_purchase_detailed": TallyPurchaseDetailed,
                'tally_purchase_return_detailed':TallyPurchaseReturnDetailed,
                "tally_sales_detailed":TallySalesDetailed,
                'tally_sales_return_detailed':TallySalesReturnDetailed,
                'tally_masters':TallyMasters,
                'tally_items':TallyItems,
                'tally_item_mapping':TallyItemsMapping,
                'tally_receipt_detailed':TallyReceipt,
                'tally_payments_detailed':TallyPayments,
                'tally_journal_detailed':TallyJournal
                }

report_table_map = {
    'sales': "tally_sales_detailed",
    'sales-return': 'tally_sales_return_detailed',
    'purchase': "tally_purchase_detailed",
    'purchase-return': 'tally_purchase_return_detailed',
    'item':"tally_items",
    'master':"tally_masters",
    'receipt':"tally_receipt_detailed",
    'payments':"tally_payments_detailed",
    'journal':'tally_journal_detailed',
}

        

tables = {**tally_tables}


current_date = datetime.today().date().strftime("%Y-%m-%d")

kb_daily_exported_data = {
    # --- FCY Companies (Top) ---

    "Frexotic Foods (FCY)": ["FCY Frexotic", "2014-04-01", current_date],
    "Kay Bee Exports (FCY) FROM 20-21": ["FCY KBE", '2020-04-01', current_date],
    "KAY BEE EXPORTS INTERNATIONAL PVT LTD (FCY)": ["FCY KBEIPL",'2022-04-01', current_date],
    "Orbit Exports (FCY)": ["FCY Orbit",'2014-04-01', current_date],
    "Kay Bee Agro International Pvt Ltd (FCY)": ["FCY KBAIPL",'2019-04-01', current_date],
    "Freshnova Pvt Ltd (FCY)": ["FCY Freshnova",'2024-04-01', current_date],

    # --- Other Companies (Middle) ---

    "KAY BEE EXPORTS INTERNATIONAL PVT LTD -Vashi": ["Vashi KBEIPL","2022-04-01", current_date],
    "Kay Bee Exports - Vashi FY 2022-23 & 23-24": ["Vashi KBE","2022-04-01", current_date],
    "Kay Bee Exports - Thane (From Apr-24)": ["Thane KBE","2024-04-01", current_date],
    "KAY BEE FRUITS INC": ["USA KB Fruits","2023-04-01", current_date],
    "Indifruit": ["Thane Indifruit","2024-04-01", current_date],
    "Perfect Produce Partners": ["Thane Perfect Produce","2024-04-01", current_date],
    "Kay Bee Fresh LLP": ["Thane KB Fresh","2015-04-01", current_date],
    "Freshnova Private Limited": ["Thane Freshnova","2013-04-01", current_date],
    "Aamrica Fresh Private Limited": ["Thane Aamrica","2024-04-01", current_date],
    "Kay Bee Agro Farms Pvt Ltd - (From 1-Apr-2016)": ["Thane KBAFPL","2016-04-01", current_date],
    "Kay Bee Veg Pvt Ltd": ["MP KBVPL","2013-04-01", current_date],
    "KAY BEE FRESH VEG & FRUIT PVT LTD": ["MP KBFV&FPL","2013-04-01", current_date],
    "Fruit & Veg Private Limited": ["MP F&VPL","2013-04-01", current_date],
    "Kay Bee Farm Management Services Pvt Ltd": ["MP KBFMSPL","2012-04-01", current_date],
    "Kay Bee Agro International Pvt Ltd (MP)": ["MP KBAIPL","2017-04-01", current_date],
    "KAY BEE EXPORTS INTERNATIONAL PVT LTD (Thane) - (from 2024)": ["Thane KBEIPL",'2024-04-01',current_date],
    "Fab Fresh Fruits": ["Thane Fab Fresh",'2024-04-01',current_date],
    "KAY BEE EXPORTS INTERNATIONAL PVT LTD (Nagar NA) - (from 1-Apr-23)": ["Nagar KBEIPL",'2024-04-01',current_date],
    "KAY BEE EXPORTS INTERNATIONAL PVT LTD (Gujarat)": ["Gujarat KBEIPL",'2022-04-01',current_date],
    "KAY BEE EXPORTS INTERNATIONAL PVT LTD (CARGO)": ["Cargo KBEIPL",'2024-04-01',current_date],
    "Kay Bee Exports - Nagar Non Agri Divsion - FY 2021-22": ["Nagar NA KBE",'2021-04-01', current_date],
    "Kay Bee Exports - Agri Div. Nagar - FY2022-23 & 2023-24": ["Nagar A KBE",'2022-04-01',current_date],
    "Kay Bee Exports - Gujarat - FY2021-22": ["Gujarat KBE",'2021-04-01', current_date],
    "KAY BEE EXPORTS-MP FY 2021-22": ["MP KBE",'2021-04-01', current_date],  
    "KAY BEE EXPORTS (JDS)": ["JDS KBE",'2021-04-01', current_date],
    "KAY BEE CARGO": ["Cargo KBE",'2021-04-01', current_date],
    "Orbit Exports (MH) from Apr-24": ["Thane Orbit",'2024-04-01',current_date],
    "Orbit Exports (Gujarat)": ["Gujarat Orbit",'2024-04-01',current_date], 
    "Frexotic Foods (From Apr-24)": ["Thane Frexotic",'2024-04-01',current_date],  
    "Kay Bee Agro International Pvt Ltd (GJ)": ["Gujarat KBAIPL",'2013-04-01',current_date],
    "Kay Bee Agro International Pvt Ltd (MH)": ["Thane KBAIPL",'2023-04-01',current_date],
    "Kay Bee veg Ltd - FY 2020-21 -(from 1-Apr-20)": ["UK KB Veg", '2020-04-01', '2025-03-31'],
    "Kay Bee veg Ltd - FY 2020-21 -(from 1-Apr-25)": ["UK KB Veg", '2025-04-01', current_date],

    # --- Phaltan Companies (Bottom) ---

    # "KAY BEE EXPORTS INTERNATIONAL PVT LTD (Phaltan NA) - (from 1-Apr-23)": ["Phaltan KBEIPL"],
    # "Kay Bee Exports - Agri Division Phaltan 21-22": ["Phaltan NA KBE"],
    # "KAY BEE EXPORTS (PHALTAN) FY21-22": ["Phaltan A KBE"],
}

