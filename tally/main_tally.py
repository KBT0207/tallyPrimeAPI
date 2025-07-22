import pyautogui as pg
import os
import time
from tally import tally_utils
from utils.common_utils import kb_daily_exported_data
from datetime import datetime
from logging_config import logger
from typing import Optional


def tally_prime_api_export_data(company: list, fromdate: str, todate: str, extra_reports:Optional[bool] = True):
    valid_companies = []
    for check_company in company:
        comp_valid = company_validation(check_company, fromdate, todate)
        if comp_valid is not None:
            valid_companies.append(comp_valid)

    from_date_str = datetime.strptime(fromdate, '%Y-%m-%d').strftime('%d-%m-%Y')
    to_date_str = datetime.strptime(todate, '%Y-%m-%d').strftime('%d-%m-%Y')
    current_date = datetime.today().date()
    current_year = current_date.year
    current_month = current_date.month
    start_date = datetime.strptime(fromdate, '%Y-%m-%d').date()
    start_year = start_date.year
    start_month = start_date.month

    start_quarter , end_quarter = get_quarter_month_range(current_date)
    

    logger.info(f"Starting Tally Prime API export from {from_date_str} to {to_date_str} for companies: {valid_companies}")

    for comp in valid_companies:
        time.sleep(1)
        logger.info(f"Processing company: {comp}")

        pg.hotkey('win', 'd')
        logger.debug("Sent hotkey to show desktop.")

        tally_utils.start_tally()
        logger.info("Tally started...")

        time.sleep(1)
        tally_utils.select_company(company_code=comp)
        mc = kb_daily_exported_data.get(comp)[0]
        logger.debug(f"Material Centre for {comp}: {mc}")
        logger.info(f"Selected company: {comp}")
    
        reports = ['sales', 'sales-return']
        if extra_reports == True:
            if (start_year == current_year) and (start_month >= start_quarter) and (current_month <= end_quarter):
                for r in ['item', 'master','outstanding']:
                    if r not in reports:
                        reports.append(r)

        logger.info(f"Starting report export for: {reports}")

        try:
            time.sleep(1)
            no_vch_entered_in_tally = 'tally/images/no_voucher_enterd_in_comp.png'
            no_vch = pg.locateOnScreen(no_vch_entered_in_tally, confidence=0.9)
            time.sleep(1)
            pg.moveTo(no_vch)
            if no_vch:
                print("image found")
                logger.warning(f"No vouchers entered for {comp}. Closing Tally and moving to the next company.")
                pg.hotkey('alt', 'f4')
                time.sleep(2)
                pg.press("y")
                time.sleep(1)
                continue
        except:       
            for report in reports:
                logger.info(f"Generating report: {report}")
                func_reports = tally_utils.tally_api_select_report(
                    report_type=report,
                    from_date=from_date_str,
                    to_date=to_date_str
                )
                logger.debug(f"Report result for {report}: {func_reports}")

                if func_reports != 'No Reports':
                    logger.info(f"Exporting data for report: {report}")
                    tally_utils.api_exports_data(
                        reports_type=report,
                        esc=4,
                        material_centre=mc,
                        todate=to_date_str
                    )
                else:
                    logger.warning(f"No reports found for {report}, skipping...")

            pg.press('esc')
            time.sleep(3)
            pg.press('y')
            logger.debug("Exited current screen in Tally.")

            pg.press('esc')
            time.sleep(3)
            pg.press('y')
            logger.debug("Exited company in Tally.")

        logger.info("All companies processed successfully.")

def company_validation(company:str, comp_fromdate: str, comp_todate: str):
    comp = kb_daily_exported_data.get(company)
    comp_start_date, comp_end_date = comp[1:3]
    from_dt = datetime.strptime(comp_fromdate, "%Y-%m-%d").date()
    to_dt = datetime.strptime(comp_todate, "%Y-%m-%d").date()
    comp_start_date = datetime.strptime(comp_start_date, '%Y-%m-%d').date()
    comp_end_date = datetime.strptime(comp_end_date, '%Y-%m-%d').date()
    if (from_dt >= comp_start_date) and (to_dt <= comp_end_date ):
        return company
    else:
        return None
    

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






    
        



