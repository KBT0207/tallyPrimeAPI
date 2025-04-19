import pyautogui as pg
import os
from dotenv import load_dotenv
import time
from busy.busy_utils import start_rdc
from logging_config import logger
from utils import common_utils
from busy.busy_utils import find_img, image_click

load_dotenv('.env')

pg.FAILSAFE = True
pg.PAUSE = 1

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
    path = r'\\ho-nas\Server Data\IT & MIS\Jovo Tally\Data'
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


def select_kbe_company(company_code):
    find_img('tally/images/tally_start.png', conf=0.95)
    time.sleep(2)
    try: 
        data_server = pg.locateOnScreen('tally/images/tally_data_server.png', confidence=0.9)
        pg.click(data_server)
        pg.click()
    except:
        pass
    find_img(f'tally/images/kbe_comp_list.png', conf=0.95)
    time.sleep(1)
    pg.typewrite(str(company_code), interval=0.2)
    find_img(f'tally/images/kbe_{company_code}.png', conf=0.95)
    pg.click()
    pg.press("enter")
    find_img('tally/images/tally_username.png')
    pg.typewrite(os.getenv('TALLY_USERNAME'), interval=0.1)
    pg.press('enter')
    pg.typewrite(os.getenv('TALLY_PASSWORD'), interval=0.1)
    pg.press('enter')

def select_report(report_type):
    find_img('tally/images/tally_gateway.png')
    pg.press("d")
    find_img('tally/images/display_reports.png')
    pg.press('a')
    time.sleep(3)
    pg.press(report_type)
    find_img('tally/images/report_particulars.png')
    pg.press('enter')
    if report_type in ['y', 'r', 'j']:
        pg.hotkey('alt','f5')
        time.sleep(3)
  
def change_period(from_date, to_date):
    find_img('tally/images/report_list.png')
    time.sleep(2)
    pg.hotkey("alt", "f2")
    pg.typewrite(from_date, interval=0.2)
    pg.press('enter')
    pg.typewrite(to_date, interval=0.2)
    pg.press('enter')

def change_receivables_period(from_date, to_date):
    find_img('tally/images/remove_line.png')
    time.sleep(2)
    pg.hotkey("alt", "f2")
    pg.typewrite(from_date, interval=0.2)
    pg.press('enter')
    pg.typewrite(to_date, interval=0.2)
    pg.press('enter')

def change_period_balance(from_date, to_date):
    find_img('tally/images/report_particulars.png')
    time.sleep(1)
    pg.hotkey("alt", "f2")
    pg.typewrite(from_date, interval=0.2)
    pg.press('enter')
    pg.typewrite(to_date, interval=0.2)
    pg.press('enter')

def change_kbe_period_balance(from_date, to_date):
    find_img('tally/images/kbe_outstanding_data.png')
    time.sleep(1)
    pg.hotkey("alt", "f2")
    pg.typewrite(from_date, interval=0.2)
    pg.press('enter')
    pg.typewrite(to_date, interval=0.2)
    pg.press('enter')

def export_report_data(path, filename):
    find_img('tally/images/report_list.png')
    time.sleep(1)
    pg.hotkey('ctrl', 'e')
    time.sleep(1.5)
    pg.press('c')
    time.sleep(2)
    pg.press('down')
    time.sleep(1)
    find_img('tally/images/export_settings.png', conf=0.95 )
    time.sleep(1)
    pg.click()
    time.sleep(1)
    pg.press('down')
    pg.press('enter')
    pg.typewrite('excel', interval=0.3)
    pg.press('enter')

    find_img("tally/images/folder_path.png")
    pg.click()
    time.sleep(1)
    pg.press('enter')
    pg.typewrite("Specify Path",interval=0.1)
    time.sleep(1)
    pg.press('enter')
    time.sleep(1)
    pg.typewrite(path, interval=0.2)
    pg.press('enter')
    time.sleep(1)
    pg.press('enter')
    time.sleep(1)
    
    pg.press('down')
    pg.press('enter')
    pg.typewrite(filename, interval=0.2)
    pg.press('enter')

    pg.hotkey("ctrl", "a")
    time.sleep(1)
    pg.press('e')

    find_img(img='tally/images/report_list.png')

def export_report_data_detailed(path, filename, mc:str):
    forex_curr = ["FCY Frexotic",
                  "FCY KBE",
                  "FCY KBEIPL",
                  "FCY Orbit",
                  'FCY KBAIPL',
                  "FCY Freshnova"
                  ]
    
    find_img('tally/images/report_list.png')
    
    time.sleep(1)
    pg.hotkey('ctrl', 'e')
    time.sleep(1.5)
    pg.press('c')
    time.sleep(2)
    pg.press('down')
    time.sleep(1)
    if any(keyword in mc for keyword in forex_curr):
        try:
            helper_forex_currency()
        except:
            pass
    find_img('tally/images/export_settings.png', conf=0.95 )
    time.sleep(1)
    pg.click()
    time.sleep(1)
    pg.press('down')
    pg.press('enter')
    pg.typewrite('excel', interval=0.3)
    pg.press('enter')

    find_img("tally/images/folder_path.png")
    pg.click()
    time.sleep(1)
    pg.press('enter')
    pg.typewrite("Specify Path",interval=0.1)
    time.sleep(1)
    pg.press('enter')
    time.sleep(1)
    pg.typewrite(path, interval=0.2)
    pg.press('enter')
    time.sleep(1)
    pg.press('enter')
    time.sleep(1)
    
    pg.press('down')
    pg.press('enter')
    pg.typewrite(filename, interval=0.2)
    pg.press('enter')
    
    pg.hotkey("ctrl", "a")
    time.sleep(1)
    pg.press('e')

    find_img(img='tally/images/report_list.png')

def export_accounts_data(path, filename):
    find_img('tally/images/accounts.png')
    time.sleep(1)
    pg.hotkey('ctrl', 'e')
    time.sleep(1.5)
    pg.press('c')
    time.sleep(2)
    pg.press('down')
    time.sleep(1)
    pg.press('enter')
    pg.typewrite( 'Name (Alias)', interval=0.2)
    pg.press("enter")
    find_img('tally/images/export_settings.png', conf=0.95 )
    time.sleep(1)
    pg.click()
    time.sleep(1)
    pg.press('down')
    pg.press('enter')
    pg.typewrite('excel', interval=0.3)
    pg.press('enter')
    find_img("tally/images/folder_path.png")
    pg.click()
    pg.press('enter')
    pg.typewrite("Specify Path",interval=0.1)
    time.sleep(1)
    pg.press('enter')
    time.sleep(1)
    pg.typewrite(path, interval=0.2)
    pg.press('enter')
    time.sleep(1)
    pg.press('enter')
    time.sleep(1)
    pg.press('down')
    pg.press('enter')
    pg.typewrite(filename, interval=0.2)
    pg.press('enter')

    pg.hotkey("ctrl", "a")
    time.sleep(1)
    pg.press('e')

    find_img(img='tally/images/accounts.png', conf=0.95)

def export_balance_data(path, filename):
    find_img('tally/images/remove_line.png')
    time.sleep(1)
    pg.hotkey('ctrl', 'e')
    time.sleep(1.5)
    pg.press('c')
    time.sleep(1.5)
    pg.press('down')
    time.sleep(1)
    find_img('tally/images/export_settings.png', conf=0.95 )
    time.sleep(1)
    pg.click()
    time.sleep(1)
    pg.press('down')
    pg.press('enter')
    pg.typewrite('excel', interval=0.3)
    pg.press('enter')

    find_img("tally/images/folder_path.png")
    pg.click()
    pg.press('enter')
    pg.typewrite(path, interval=0.2)
    pg.press('enter', presses=2, interval=0.4)
    
    pg.press('down')
    pg.press('enter')
    pg.typewrite(filename, interval=0.2)
    pg.press('enter')

    pg.hotkey("ctrl", "a")
    time.sleep(1)
    pg.press('e')

    find_img(img='tally/images/remove_line.png', conf=0.95)

def export_kbe_balance_data(path, filename):
    find_img('tally/images/remove_line.png')
    time.sleep(1)
    pg.hotkey('ctrl', 'e')
    time.sleep(1.5)
    pg.press('c')
    time.sleep(1.5)
    pg.press('down')
    time.sleep(1)
    find_img('tally/images/export_settings.png', conf=0.95 )
    time.sleep(1)
    pg.click()
    time.sleep(1)
    pg.press('down')
    pg.press('enter')
    pg.typewrite('excel', interval=0.3)
    pg.press('enter')
    time.sleep(1.5)
    try:
        show_currency = pg.locateOnScreen(image= 'tally/images/show_currency.png', confidence= 0.9)
        pg.click(show_currency)
        pg.press('enter')
        print("changed currency to be yes")
    except:
        print('passed')
        pass

    find_img("tally/images/folder_path.png")
    pg.click()
    pg.press('enter')
    pg.typewrite(path, interval=0.2)
    pg.press('enter', presses=2, interval=0.4)
    
    pg.press('down')
    pg.press('enter')
    pg.typewrite(filename, interval=0.2)
    pg.press('enter')

    pg.hotkey("ctrl", "a")
    time.sleep(1)
    pg.press('e')

    find_img(img='tally/images/remove_line.png', conf=0.95)

def back_to_tally_home(times):
    for _ in range(1, times+1):
        pg.press('esc')
        time.sleep(3)

def change_company():
    find_img('tally/images/tally_gateway.png')
    time.sleep(1)
    pg.hotkey('alt', 'f1')
    time.sleep(1)
    pg.press('y')
    time.sleep(1)
    pg.press('enter')

def accounts():
    find_img('tally/images/tally_gateway.png')
    pg.press('h')
    time.sleep(1.5)
    pg.typewrite('ledgers', interval=0.1)
    pg.press('enter')
    find_img(img='tally/images/ledgers_list.png')
    pg.press('f5')
    time.sleep(1)
    
def items():
    find_img('tally/images/tally_gateway.png')
    pg.press('h')
    time.sleep(1.5)
    pg.typewrite('stock items', interval=0.1)
    pg.press('enter')
    find_img(img='tally/images/accounts.png')
    pg.press('f5')
    time.sleep(2.5)

def outstanding_balance():
    find_img('tally/images/tally_gateway.png')
    pg.press('b')
    time.sleep(1.5)
    try:
        assets = pg.locateOnScreen('tally/images/current_assets.png', confidence=0.9)
        pg.click(assets, duration=0.2)
        pg.press('enter')
    except:
        pg.locateOnScreen('tally/images/sel_current_assets.png', confidence=0.9)
        pg.press('enter')
    try:
        sundry = pg.locateOnScreen('tally/images/sundry.png', confidence=0.9)
        pg.click(sundry, duration=0.2)
        pg.press('enter')
    except:
        pg.locateOnScreen('tally/images/sel_sundry.png', confidence=0.9)
        pg.press('enter')

    pg.press('f12')
    find_img('tally/images/grouping.png')
    pg.click()
    pg.typewrite('ledger')
    pg.press('enter')

    find_img('tally/images/display_name_balance.png')
    pg.click()
    pg.typewrite('name only')
    pg.press('enter')
    pg.hotkey('ctrl', 'a')

def kbe_outstanding_balance():
    find_img('tally/images/tally_gateway.png')
    pg.press('d')
    time.sleep(1.5)
    pg.press('s')
    time.sleep(1.5)
    pg.press('o')
    time.sleep(1.5)
    pg.press('r')
    time.sleep(1.5)

def receivables():
    find_img('tally/images/tally_gateway.png')
    pg.press('d')
    pg.press('s')
    time.sleep(0.3)
    pg.press('o')
    time.sleep(0.3)
    pg.press('g')
    pg.typewrite('sundry debtors', interval=0.2)
    pg.press('enter')
    find_img('tally/images/report_particulars.png')
    pg.press('f5')
    time.sleep(1)
    pg.hotkey('ctrl', 'f8')
    
def exporting_reports(report:str, from_date:str, to_date:str,  path:str, filename:str, esc:int):
    time.sleep(1)
    select_report(report_type= report)
    time.sleep(1)
    change_period(from_date= from_date , to_date= to_date) 
    time.sleep(1)
    export_report_data(path= path, filename= filename)
    time.sleep(3)
    back_to_tally_home(times=esc)

def fcy_exporting_reports(report:str, from_date:str, to_date:str,  path:str, filename:str, esc:int):
    time.sleep(1)
    select_report(report_type= report)
    time.sleep(1)
    change_period(from_date= from_date , to_date= to_date) 
    time.sleep(1)
    fcy_export_report_data(path= path, filename= filename)
    time.sleep(1.5)
    back_to_tally_home(times=esc)
    
def helper_forex_currency():
    while True:
        try:
            time.sleep(1)
            loc = pg.locateOnScreen(r'tally/images/forex.png', confidence=0.9)
            if loc:
                pg.click(loc)
                time.sleep(1)
                pg.press('enter')
                break
        except pg.ImageNotFoundException:
            print("Forex image not found, retrying...")
        except Exception as e:
            print(f"Unexpected error: {e}")
        time.sleep(1)

def fcy_export_report_data(path, filename):
    find_img('tally/images/report_list.png')
    time.sleep(1)
    pg.hotkey('ctrl', 'e')
    time.sleep(1.5)
    pg.press('c')
    time.sleep(2)
    pg.press('down')
    time.sleep(1)
    helper_forex_currency()
    time.sleep(1)
    find_img('tally/images/export_settings.png', conf=0.95 )
    time.sleep(1)
    pg.click()
    time.sleep(1)
    pg.press('down')
    pg.press('enter')
    pg.typewrite('excel', interval=0.3)
    pg.press('enter')

    find_img("tally/images/folder_path.png")
    pg.click()
    time.sleep(1)
    pg.press('enter')
    pg.typewrite("Specify Path",interval=0.2)
    time.sleep(1)
    pg.press('enter')
    time.sleep(1)
    pg.typewrite(path, interval=0.2)
    pg.press('enter')
    time.sleep(1)
    pg.press('enter')
    time.sleep(1)
    
    pg.press('down')
    pg.press('enter')
    pg.typewrite(filename, interval=0.2)
    pg.press('enter')

    pg.hotkey("ctrl", "a")
    time.sleep(1)
    pg.press('e')

    find_img(img='tally/images/report_list.png')
    
def exporting_reports_detaild(report:str, from_date:str, to_date:str,  path:str, filename:str, esc:int, mc:str):
    time.sleep(1)
    select_report(report_type= report)
    time.sleep(1)
    change_period(from_date= from_date , to_date= to_date) 
    time.sleep(1)
    columner()
    time.sleep(1)
    export_report_data_detailed(path= path, filename= filename, mc=mc)
    time.sleep(1.5)
    back_to_tally_home(times=esc)
    

def columner():
    time.sleep(0.6)
    pg.press('f8')
    
    find_img("tally/images/columnr.png")

    image_click(img_path='tally/images/vch_type.png', key_press='y')
    time.sleep(0.5)
    image_click(img_path='tally/images/vch_no.png', key_press='y')
    time.sleep(0.5)
    image_click(img_path='tally/images/vch_ref.png', key_press='y')
    time.sleep(1)

    try:
        ref_date = pg.locateOnScreen('tally/images/vch_ref_date.png', confidence=0.9)
        time.sleep(0.5)
        if ref_date:
            pg.click(ref_date)
            time.sleep(1)
            pg.typewrite('y')
            time.sleep(0.5)
            pg.press('enter')
    except Exception as e:
        print(f"[!] Error locating ref_date: {e}")

    image_click(img_path='tally/images/qty_details.png', key_press='y')
    time.sleep(0.5)
    pg.typewrite('n', interval=0.1)
    time.sleep(0.5)
    pg.press('enter')

    for _ in range(3):
        pg.typewrite('y', interval=0.3)
        time.sleep(0.5)
        pg.press('enter')

    time.sleep(2)
    pg.hotkey('ctrl', 'a')
    time.sleep(1)
    pg.hotkey('alt', 'f5')
    time.sleep(1)
