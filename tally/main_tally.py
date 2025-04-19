import pyautogui as pg
import os
import time
from tally import tally_utils
from utils.common_utils import tally_reports,company_dict_kaybee_exports, fcy_company, tally_reports_detailed,all_columner_comp
from datetime import datetime, timedelta
from logging_config import logger




def exporting_data(company, fromdate:str, todate:str, filename:str):
    from_date_str = datetime.strptime(fromdate, '%Y-%m-%d').strftime('%d-%m-%Y')
    to_date_str = datetime.strptime(todate, '%Y-%m-%d').strftime('%d-%m-%Y')
    for comp_name in company:
        time.sleep(2)
        pg.hotkey("win", "d")
        time.sleep(1)
        tally_utils.start_tally()
        logger.info("Tally started...")
        time.sleep(1)
        mc_name = company_dict_kaybee_exports.get(comp_name, "Unknown_Company") 
        
        logger.info(f"{comp_name} selected...")
        
        tally_utils.select_company(company_code= comp_name)
        
        logger.info(f"{comp_name} selected...")
        
        for rep in list(tally_reports.keys()):
            path= fr"E:\automated_tally_downloads\{mc_name}\{tally_reports[rep]}"
            os.makedirs(path, exist_ok=True)
            tally_utils.exporting_reports(report= rep, 
                        from_date= from_date_str, to_date= to_date_str,
                        path= fr"E:\automated_tally_downloads\{mc_name}\{tally_reports[rep]}",
                        filename= f"{mc_name.replace(' ', '_')}_{tally_reports[rep]}_{filename}.xlsx", 
                        esc= 4)
            logger.info(f"Exported {tally_reports[rep]} of {mc_name} of {filename}")
                    
        # tally_utils.accounts()
        # path1 = fr"E:\automated_tally_downloads\{mc_name}\accounts"
        # os.makedirs(path1, exist_ok=True)
        # tally_utils.export_accounts_data(path= fr"E:\automated_tally_downloads\{mc_name}\accounts",
        #                 filename= f"{mc_name}_accounts_{filename}.xlsx")    

        # time.sleep(2)
        # pg.press('esc')
        # time.sleep(2)
        # pg.press('esc')
        # logger.info(f"Exported accounts of {mc_name} of {filename}")

        # tally_utils.change_company()
    
        # time.sleep(4)
        # pg.press('esc')
        # time.sleep(4)
        # pg.press('y')
        tally_utils.while_close_tally()
    
        logger.info("Tally closed ...")

def exporting_outstanding_balance(company:list, dates:list, monthly:bool):
    pg.hotkey("win", "d")
    
    tally_utils.start_tally()
    logger.info("Tally started...")

    for comp in company:
        tally_utils.select_company(company_code= comp)
        logger.info(f"{comp} selected...")
        
        tally_utils.outstanding_balance()
        if monthly:

            first_day_of_current_month = datetime.today().replace(day=1)
            previous_month = (first_day_of_current_month - timedelta(days=1)).strftime('%B-%Y')
            file_path = fr"D:\monthly_data\{comp}\outstanding\{previous_month}"
            if not os.path.exists(file_path):
                os.makedirs(file_path)
        else:
            file_path = fr"D:\automated_tally_downloads\{comp}\outstanding"
        for date in dates:
            tally_utils.change_period_balance(from_date= '01-04-2024', to_date= date)
            tally_utils.export_balance_data(path= file_path, 
                                            filename= f"{comp}_outstanding_{date}.xlsx")
            time.sleep(1.5)

        tally_utils.back_to_tally_home(times= 3)
        logger.info(f"Exported outstanding balance of {comp} of {date}")

        tally_utils.change_company()
    
    time.sleep(2)
    pg.press('esc')
    time.sleep(2)
    pg.press('y')
    logger.info("Tally closed ...")

def exporting_receivables(company:list, dates:list, monthly:bool):
    pg.hotkey("win", "d")
    
    tally_utils.start_tally()
    logger.info("Tally started...")

    for comp in company:
        tally_utils.select_company(company_code= comp)
        logger.info(f"{comp} selected...")
        
        tally_utils.receivables()
        if monthly:

            first_day_of_current_month = datetime.today().replace(day=1)
            previous_month = (first_day_of_current_month - timedelta(days=1)).strftime('%B-%Y')
            file_path = fr"D:\monthly_data\{comp}\receivables\{previous_month}"
            if not os.path.exists(file_path):
                os.makedirs(file_path)
        else:
            file_path = fr"D:\automated_tally_downloads\{comp}\receivables"
        
        for date in dates:
            tally_utils.change_receivables_period(from_date= '01-04-2024', to_date= date)
            tally_utils.export_balance_data(path= fr"D:\monthly_data\{comp}\receivables",
                            filename= f"{comp}_receivables_{date}.xlsx")
            time.sleep(1)

        tally_utils.back_to_tally_home(times= 6)
        logger.info(f"Exported receivables of {comp} of {date}")

        tally_utils.change_company()
    
    time.sleep(2)
    pg.press('esc')
    time.sleep(2)
    pg.press('y')
    logger.info("Tally closed ...")

def exporting_kbe_outstanding(company:list, dates:list):
    pg.hotkey("win", "d")
    
    tally_utils.start_tally()
    logger.info("Tally started...")

    for comp in company:
        tally_utils.select_kbe_company(company_code= comp)
        logger.info(f"{comp} selected...")
        
        tally_utils.kbe_outstanding_balance()
        file_path = fr"D:\automated_kbe_downloads\{comp}\outstanding"

        for date in dates:
            tally_utils.change_kbe_period_balance(from_date= '01-04-2024', to_date= date)
            tally_utils.export_kbe_balance_data(path= file_path, 
                                            filename= f"{comp}_kbe_outstanding_{date}.xlsx")
            time.sleep(1.5)

        tally_utils.back_to_tally_home(times= 4)
        logger.info(f"Exported outstanding balance of {comp} of {date}")

        tally_utils.change_company()
    
    time.sleep(2)
    pg.press('esc')
    time.sleep(2)
    pg.press('y')
    logger.info("Tally closed ...")

def exporting_kbe_accounts(company, filename:str):
    pg.hotkey("win", "d")

    tally_utils.start_tally()
    logger.info("Tally started...")

    for comp in company:
        tally_utils.select_kbe_company(company_code= comp)
        logger.info(f"{comp} selected...")

        tally_utils.accounts()
        tally_utils.export_accounts_data(path= fr"D:\automated_kbe_downloads\{comp}\accounts",
                        filename= f"{comp}_kbe_accounts_{filename}.xlsx")    

        time.sleep(2)
        pg.press('esc')
        time.sleep(2)
        pg.press('esc')
        logger.info(f"Exported accounts of {comp} of {filename}")

        tally_utils.change_company()
    
    time.sleep(2)
    pg.press('esc')
    time.sleep(2)
    pg.press('y')
    logger.info("Tally closed ...")
    
def fcy_exporting_data(company, fromdate:str, todate:str, filename:str):
    from_date_str = datetime.strptime(fromdate, '%Y-%m-%d').strftime('%d-%m-%Y')
    to_date_str = datetime.strptime(todate, '%Y-%m-%d').strftime('%d-%m-%Y')
    
    for comp_name in company:
        time.sleep(2)
        pg.hotkey("win", "d")
        time.sleep(1)
        tally_utils.start_tally()
        logger.info("Tally started...")
        time.sleep(1)
        mc_name = fcy_company.get(comp_name, "Unknown_Company") 
        logger.info(f"{comp_name} selected...")
        
        tally_utils.select_company(company_code= comp_name)
        
        logger.info(f"{comp_name} selected...")
        
        for rep in list(tally_reports.keys()):
            path= fr"E:\automated_tally_downloads\{mc_name}\{tally_reports[rep]}"
            os.makedirs(path, exist_ok=True)
            tally_utils.fcy_exporting_reports(report= rep, 
                        from_date= from_date_str, to_date= to_date_str,
                        path= fr"E:\automated_tally_downloads\{mc_name}\{tally_reports[rep]}",
                        filename= f"{mc_name.replace(' ', '_')}_{tally_reports[rep]}_{filename}.xlsx", 
                        esc= 4)
            logger.info(f"Exported {tally_reports[rep]} of {mc_name} of {filename}")
                    
        # tally_utils.accounts()
        # path1 = fr"E:\automated_tally_downloads\{mc_name}\accounts"
        # os.makedirs(path1, exist_ok=True)
        # tally_utils.export_accounts_data(path= fr"E:\automated_tally_downloads\{mc_name}\accounts",
        #                 filename= f"{mc_name}_accounts_{filename}.xlsx")    

        # time.sleep(2)
        # pg.press('esc')
        # time.sleep(2)
        # pg.press('esc')
        # logger.info(f"Exported accounts of {mc_name} of {filename}")
        # time.sleep(2)
        # pg.press('esc')
        # time.sleep(2)
        # pg.press('esc')
        # logger.info(f"Exported accounts of {mc_name} of {filename}")

        # # tally_utils.change_company()
    
        
        tally_utils.while_close_tally()
        time.sleep(2)

    
    
        logger.info("Tally closed ...")

def exporting_data_detailed(company, fromdate:str, todate:str, filename:str):
    from_date_str = datetime.strptime(fromdate, '%Y-%m-%d').strftime('%d-%m-%Y')
    to_date_str = datetime.strptime(todate, '%Y-%m-%d').strftime('%d-%m-%Y')
    for comp_name in company:
        time.sleep(2)
        pg.hotkey("win", "d")
        time.sleep(1)
        tally_utils.start_tally()
        logger.info("Tally started...")
        time.sleep(1)
        mc_name = all_columner_comp.get(comp_name, "Unknown_Company") 
        
        logger.info(f"{comp_name} selected...")
        
        tally_utils.select_company(company_code= comp_name)
        
        logger.info(f"{comp_name} selected...")
        
        for rep in list(tally_reports_detailed.keys()):
            path= fr"E:\automated_tally_downloads\{mc_name}\{tally_reports_detailed[rep]}"
            os.makedirs(path, exist_ok=True)
            print(path)
            tally_utils.exporting_reports_detaild(report= rep, 
                        from_date= from_date_str, to_date= to_date_str,
                        path= fr"E:\automated_tally_downloads\{mc_name}\{tally_reports_detailed[rep]}",
                        filename= f"{mc_name.replace(' ', '_')}_{tally_reports_detailed[rep]}_{filename}.xlsx", 
                        esc= 4,
                        mc=mc_name)
            
            logger.info(f"Exported {tally_reports_detailed[rep]} of {mc_name} of {filename}")
                    
        tally_utils.while_close_tally()
        time.sleep(2)
    
        logger.info("Tally closed ...")