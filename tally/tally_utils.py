import pyautogui as pg
import os
from dotenv import load_dotenv
import time
# from busy.busy_utils import start_rdc
from logging_config import logger
from utils import common_utils
from tally.api_utils import rename_latest_file,select_all_data
from datetime import datetime

from typing import Union
from typing import Optional

load_dotenv('.env')

pg.FAILSAFE = True
pg.PAUSE = 1

def back_to_tally_home(times):
    for _ in range(1, times+1):
        pg.press('esc')
        time.sleep(4)

def image_click(img_path:str, key_press:str):
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen(img_path, confidence=0.9)
            if location:
                pg.click(location)
                time.sleep(0.5)
                pg.typewrite(key_press)
                time.sleep(0.5)
                pg.press('enter')
                time.sleep(0.5)
        except:
            continue
    pg.moveTo(location,duration=0.1)

def find_img(img:str, timeout:int = None, conf: Union[float, int] = 0.9, gs:bool=False ) -> None:
    """Function will continue to look for the image for the time given as timeout parameter seconds (default is 10 secs).

    Args:
        img (str): The image you want to find.
        timeout(int): Amount of seconds it should take to find the image the image 
                    if None is given then it waits indefinetly. Defaults to None
        conf (float, optional): Confidence parameter same as found in 
                    location methods in Pyautogui. Defaults to 0.9.
        gs(bool, optional): Grayscale property applied to image or not. Defaults to False 
    """
    location = None
    start_time = time.time()
    while (location == None) and (timeout is None or (time.time() - start_time) < timeout):
        try:
            location = pg.locateOnScreen(img, confidence= conf, grayscale=gs)
        except Exception:
            continue
    pg.moveTo(location,duration=0.1)

def forex_transaction_click_yes(report_type):
    pg.hotkey("ctrl", 'b')
    time.sleep(2)

    if report_type == 'outstanding':
        img_path = 'tally/images/outstanding_curr_enable.png'
    else:
        img_path = 'tally/images/forex.png'

    loc = None

    while loc is None:
        try:
            loc = pg.locateOnScreen(img_path, confidence=0.9)
            if loc:
                time.sleep(1)

                if report_type == 'outstanding':
                    pg.click(loc)
                    time.sleep(1)
                    pg.press("enter")
                else:
                    pg.press("enter")

                time.sleep(1)
                pg.hotkey("ctrl", 'a')
        except Exception as e:
            print(f"Error during forex transaction click: {e}")
        time.sleep(0.5)

def while_close_tally():
    loc = None
    while loc == None:
        try:
            loc = pg.locateOnScreen("tally/images/quit.png",confidence=0.9)
            if loc:
                pg.press('y')
        except Exception as e:
            pg.press('esc')
            time.sleep(3)

def close_rdc() -> None:
    """Closes the RDC if its running.
    """
    if not common_utils.is_process_running('mstsc.exe'):
        print("RDC alrady closed!")
    else:
        pg.press("win")
        power = pg.locateCenterOnScreen('busy/images/rdc_power_button.png')
        pg.click(power)
        find_img('busy/images/disconnect.png')
        pg.click()
        time.sleep(2)

def start_tally() -> None:
    pg.hotkey('win', 'r')
    time.sleep(1)
    pg.typewrite(r"C:\Program Files\TallyPrime\tally.exe", interval=0.1)
    pg.press('enter') 
       
def tally_data_server():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('tally/images/tally_data_server1.png', confidence= 0.9)
            if location:
                time.sleep(1)
                pg.click(location)
                time.sleep(1)
                pg.press('enter')
            else:
                logger.info("Not Found Server")
        except:
            time.sleep(1)

def specify_path():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('tally/images/specify_path.png', confidence= 0.9)
            if location:
                time.sleep(1)
                pg.click(location)
                time.sleep(1)
                pg.press('enter')
            else:
                logger.info("Not Found Server")
        except:
            time.sleep(1)
            
def ho_server():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('tally/images/ho_server.png', confidence= 0.9)
        except:
            time.sleep(1)

def phaltan_rdc():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('tally/images/phaltan_rdc.png', confidence= 0.9)
        except:
            time.sleep(1)
    
def select_company(company_code):
    path = r'\\HO-NAS\Server Data\IT & MIS\Jovo Tally\Data'
    phaltan_rdc_comp = ['KAY BEE EXPORTS INTERNATIONAL PVT LTD (Phaltan NA) - (from 1-Apr-23)', 'Kay Bee Exports - Agri Division Phaltan 21-22', 'KAY BEE EXPORTS (PHALTAN) FY21-22']
    if company_code in phaltan_rdc_comp:
        specify_path()
        time.sleep(1)
        pg.typewrite(path, interval=0.2)
        pg.press('enter')
        time.sleep(1)
        phaltan_rdc()
        time.sleep(1)
    else:
        tally_data_server()
        time.sleep(1)
        ho_server()
        time.sleep(1)

    find_img('tally/images/tally_start.png', conf=0.95)
    time.sleep(1)
    pg.typewrite(company_code, interval=0.2)
    time.sleep(1)
    pg.press("enter")
    find_img('tally/images/tally_username.png')
    pg.typewrite(os.getenv('TALLY_USERNAME'), interval=0.1)
    pg.press('enter')
    pg.typewrite(os.getenv('TALLY_PASSWORD'), interval=0.1)
    pg.press('enter')
    find_img('tally/images/tally_gateway.png')  

def APIchange_period(from_date, to_date, img: Optional[str] = None):
    first_image = img if img else 'tally/images/apiChangeDate.png'
    find_img(first_image)
    time.sleep(2)
    pg.hotkey("alt", "f2")
    pg.typewrite(from_date, interval=0.2)
    pg.press('enter')
    time.sleep(1)
    pg.typewrite(to_date, interval=0.2)
    time.sleep(1)
    pg.press('enter')
    time.sleep(1)
    find_img('tally/images/data_get.png')

def tally_api_select_report(report_type, from_date, to_date):
    find_img('tally/images/tally_gateway.png')
    time.sleep(2)
    pg.press("t")
    find_img('tally/images/tallyPrimeAPI.png')
    pg.press('g')
    time.sleep(1)
    find_img('tally/images/tallyAPIGet.png')
    time.sleep(1)
    report_functions = {
        'sales': api_helper_sales,
        'sales-return': api_helper_sales_return,
        'purchase': api_helper_purchase,
        'purchase-return': api_helper_purchase_return,
        'receipt': api_helper_receipt,
        'payments': api_helper_payments,
        'journal': api_helper_journal,
        'item': api_helper_item,
        'master': api_helper_master,
        'outstanding': api_helper_outstanding,
    }
    helper_function = report_functions.get(report_type)
    if helper_function:
        return helper_function(from_date, to_date)
    else:
        raise ValueError(f"Invalid report_type: {report_type}")
    
def api_helper_outstanding(fromdate, to_date):
    pg.press('e')
    time.sleep(1)
    find_img('tally/images/getAPIDataTypeReport.png')
    time.sleep(1)
    try:
        time.sleep(1)
        pg.locateOnScreen("tally/images/disable_outstanding.png")
        time.sleep(1)
        pg.press("esc",presses=3,interval=2)
        return 'No Reports'
    except:
        pg.press('p')
        time.sleep(1)
        find_img('tally/images/getAPIDataTypeReport.png')
        time.sleep(1)
        pg.press('u')
        time.sleep(2)
        try:
            pg.locateOnScreen("tally/images/no_access.png",confidence=0.9)
            pg.press("esc",presses=5,interval=2)
            return 'No Reports'
        except Exception as e:
            APIchange_period(from_date=fromdate, to_date=to_date, img="tally/images/apiOutstandingChangeDate.png")
            return None

def api_helper_sales(fromdate, to_date):
    pg.press('down')
    time.sleep(1)
    pg.press("enter")
    time.sleep(1)
    find_img('tally/images/getAPIDataType.png')
    time.sleep(1)
    try:
        time.sleep(1)
        pg.locateOnScreen("tally/images/disable_sales.png")
        time.sleep(1)
        pg.press("esc",presses=3,interval=2)
        return 'No Reports'
    except:
        pg.press('u')
        time.sleep(1)
        APIchange_period(from_date=fromdate, to_date=to_date)
        return None

def api_helper_sales_return(fromdate, to_date):
    pg.press('down')
    time.sleep(1)
    pg.press("enter")
    find_img('tally/images/getAPIDataType.png')
    time.sleep(1)
    try:
        time.sleep(1)
        pg.locateOnScreen("tally/images/disable_sales_return.png")
        time.sleep(1)
        pg.press("esc",presses=3,interval=2)
        return 'No Reports'
    except:
        pg.press('l')
        time.sleep(1)
        APIchange_period(from_date=fromdate, to_date=to_date)
        return None

def api_helper_purchase(fromdate, to_date):
    pg.press('p')
    time.sleep(1)
    find_img('tally/images/getAPIPurchase.png')
    time.sleep(1)
    try:
        time.sleep(1)
        pg.locateOnScreen("tally/images/disable_purchase.png")
        time.sleep(1)
        pg.press("esc",presses=3,interval=2)
        return 'No Reports'
    except:
        pg.press('u')
        time.sleep(1)
        APIchange_period(from_date=fromdate, to_date=to_date)
        return None

def api_helper_purchase_return(fromdate, to_date):
    pg.press('p')
    time.sleep(1)
    find_img('tally/images/getAPIPurchase.png')
    time.sleep(1)
    try:
        time.sleep(1)
        pg.locateOnScreen("tally/images/disable_purchase_return.png")
        time.sleep(1)
        pg.press("esc",presses=3,interval=2)
        return 'No Reports'
    except:
        pg.press('l')
        time.sleep(1)
        APIchange_period(from_date=fromdate, to_date=to_date)
        return None

def api_helper_receipt(fromdate, to_date):
    pg.press('b')
    time.sleep(1)
    find_img('tally/images/getAPIBanking.png')
    time.sleep(2)
    try:
        time.sleep(1)
        pg.locateOnScreen("tally/images/disable_receipt.png")
        time.sleep(1)
        pg.press("esc",presses=3,interval=2)
        return 'No Reports'

    except:
        pg.press('u')
        time.sleep(1)
        APIchange_period(from_date=fromdate, to_date=to_date)
        return None

def api_helper_payments(fromdate, to_date):
    pg.press('b')
    time.sleep(1)
    find_img('tally/images/getAPIBanking.png')
    time.sleep(1)
    try:
        time.sleep(1)
        pg.locateOnScreen("tally/images/disable_payment.png")
        time.sleep(1)
        pg.press("esc", presses=3, interval=2)
        return 'No Reports'
    except:
        pg.press('p')
        time.sleep(1)
        APIchange_period(from_date=fromdate, to_date=to_date)
        return None

def api_helper_journal(fromdate, to_date):
    pg.press('o')
    time.sleep(1)
    find_img('tally/images/getAPIBanking.png')
    time.sleep(1)
    try:
        time.sleep(1)
        pg.locateOnScreen("tally/images/disable_journal.png")
        time.sleep(1)
        pg.press("esc",presses=3,interval=2)
        return 'No Reports'
    except:
        pg.press('u')
        time.sleep(1)
        APIchange_period(from_date=fromdate, to_date=to_date)
        return None

def api_helper_item(fromdate, to_date):
    pg.press('m')
    time.sleep(1)
    find_img('tally/images/getAPIMaster.png')
    time.sleep(1)
    try:
        time.sleep(1)
        pg.locateOnScreen("tally/images/disable_item.png")
        time.sleep(1)
        pg.press("esc",presses=3,interval=2)
        return 'No Reports'
    except:
        pg.press('u')
        time.sleep(1)
        find_img('tally/images/item.png')
        return None

def api_helper_master(fromdate, to_date):
    pg.press('m')
    time.sleep(1)
    find_img('tally/images/getAPIMaster.png')
    time.sleep(1)
    try:
        time.sleep(1)
        pg.locateOnScreen("tally/images/disable_master.png")
        time.sleep(1)
        pg.press("esc",presses=3,interval=2)
        return 'No Reports' 
    except:
        pg.press('p')
        time.sleep(1)
        find_img('tally/images/master.png')
        return None

def api_exports_data(material_centre: str, todate, reports_type: str, esc: int):
    fcy_list = ["FCY Freshnova", "FCY Frexotic", "FCY KBE", "FCY KBEIPL", "FCY Orbit", "FCY KBAIPL"]

    invalid_report_types = {"item", "master"}

    if any(fcy in material_centre for fcy in fcy_list) and reports_type not in invalid_report_types:
            forex_transaction_click_yes(report_type=reports_type)


    try:
        todate = datetime.strptime(todate, '%d-%m-%Y').date()
    except ValueError as e:
        logger.error(f"Invalid date format: {todate}. Expected 'dd-mm-yyyy'. Error: {e}")
        return

    esc = int(esc)
    BASE_DIR = r'E:\api_download'

    # Hotkey mappings
    hotkeys = {
        'sales': ('alt', 'j'),
        'sales-return': ('alt', 'u'),
        'receipt': ('alt', 'u'),
        'payments': ('alt', 'u'),
        'journal': ('alt', 'u'),
        'purchase': ('alt', 'l'),
        'purchase-return': ('alt', 'l'),
        'item': ('alt', 'v'),
        'master': ('alt', 'j'),
        'outstanding': ('alt', 's'),
    }

    hotkey = hotkeys.get(reports_type)
    if hotkey is None:
        logger.warning(f"Unknown report type: {reports_type}")
        return

    try:
        time.sleep(3)
        if reports_type == 'item':
            target_img = pg.locateOnScreen('tally/images/target_item.png', confidence=0.9)
        elif reports_type == 'master':
            target_img = pg.locateOnScreen('tally/images/target_master.png', confidence=0.9)
        else:
            target_img = pg.locateOnScreen('tally/images/no_blank.png', confidence=0.9)

        if target_img:
            pg.moveTo(target_img, duration=0.2)
            time.sleep(1)
            pg.hotkey('ctrl', 'space')
            time.sleep(1)
            pg.hotkey(*hotkey)
            time.sleep(2)
            find_img('tally/images/upload_success.png')
            time.sleep(2)
            rename_latest_file(
                base_dir=BASE_DIR,
                material_centre=material_centre,
                report_type=reports_type,
                today=todate
            )
            time.sleep(1)
            esc += 2
            back_to_tally_home(esc)
            logger.info(f"File renamed for {material_centre} and report type '{reports_type}'")
            logger.info(f"{material_centre} exported successfully for report '{reports_type}'")
        else:
            logger.info("No blank voucher found.")
    except Exception as e:
        back_to_tally_home(esc)
        logger.warning(f"Voucher export failed for {material_centre} and report type {reports_type}: {e}")



