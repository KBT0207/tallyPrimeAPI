import pyautogui as pg
import time
from busy import busy_utils
from dotenv import load_dotenv
from datetime import datetime, timedelta



load_dotenv()



pg.PAUSE = 1.0


def select_transaction():
    transaction = pg.moveTo(241, 29, duration=0.5) 
    location = None
    print('run succsesfully')
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/trans_check.png', confidence= 0.9)
        except Exception:
            pg.click(transaction)
            time.sleep(1) 
            pass
    busy_utils.find_img('busy/images/trans_check.png', conf= 0.9)
    time.sleep(2)
    

def select_masters():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/busy_administration.png', confidence= 0.9)
            pg.click(location)   
        except Exception:
            try:
                location = pg.locateOnScreen('busy/images/busy_sel_administration.png', confidence= 0.9)
            except Exception:
                pass


def select_accounts():
    try:
        pg.locateOnScreen('busy/images/busy_sel_masters.png', confidence=0.9)
        pg.press('enter')   #enter to go in open masters
        time.sleep(0.4) 
        pg.press("enter")   #enter to go in accounts
        time.sleep(0.4)
        pg.press("down")   #down for list
        time.sleep(0.4)
        pg.press("enter")  #enter to select list 
        time.sleep(0.4)
    except:
        master = pg.locateOnScreen('busy/images/busy_masters.png', confidence=0.9)
        pg.click(master)
        time.sleep(0.4)
        pg.press("down") #down for accounts
        time.sleep(0.4)
        pg.press("down")   #down for list
        time.sleep(0.4)
        pg.press("enter")  #enter to select list 
        time.sleep(0.4)
        
    busy_utils.find_img('busy/images/standard_format.png')
    pg.click()
    pg.click()
    time.sleep(5)

    pg.typewrite('new')
    pg.press('enter')

    pg.typewrite("<<-ALL->>")
    time.sleep(0.3)
    pg.press('enter')

    pg.press('y')
    pg.press('enter')

    pg.press('f2')



def select_items():
    try:
        pg.locateOnScreen('busy/images/busy_sel_masters.png', confidence=0.9)
        pg.press('enter')   #enter to go in open masters
        time.sleep(0.4)    
    except:
        master = pg.locateOnScreen('busy/images/busy_masters.png', confidence=0.9)
        pg.click(master)
        time.sleep(0.4)
    try:
        item = pg.locateOnScreen('busy/images/busy_item.png', confidence=0.9)
        pg.click(item, duration=0.4)
    except:
        item_sel = pg.locateOnScreen('busy/images/busy_sel_item.png', confidence=0.9)
        pg.doubleClick(item_sel, duration=0.4)
    pg.press('down')
    pg.press('down')
    pg.press('enter')

    busy_utils.find_img('busy/images/standard_format.png')
    pg.click()
    pg.click()
    time.sleep(5)

    pg.typewrite('standard')
    pg.press('enter')

    pg.typewrite("<<-ALL->>")
    time.sleep(0.3)
    pg.press('enter')
    time.sleep(0.5)

    pg.press('n')
    time.sleep(0.5)
    pg.press('enter')
    time.sleep(0.5)
    pg.press('y')
    time.sleep(0.5)
    pg.press('enter')
    time.sleep(0.5)
    pg.press('f2')



def select_sales_list():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/busy_sales.png', confidence=0.9)
            pg.click(location)
            pg.press('down')
            pg.press('down')
            pg.press('enter')
        except Exception:
            time.sleep(2)
            pass
            

def select_mitp_list():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images//mitp.png', confidence=0.9)
            pg.click(location)
            pg.press('down')
            pg.press('down')
            pg.press('enter')
        except Exception:
            time.sleep(2)
            pass


def select_salesreturn_list():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/salesreturn.png', confidence=0.9)
            pg.click(location)
            pg.press('down')
            pg.press('down')
            pg.press('enter')
        except Exception:
            time.sleep(2)
            pass


def select_purchase_list():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/busy_purchase.png', confidence=0.9)
            pg.click(location)
            pg.press('down')
            pg.press('down')
            pg.press('enter')
        except Exception:
            time.sleep(2)
            pass

def select_purchase_return_list():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/busy_purchase_return.png', confidence=0.9)
            pg.click(location)
            pg.press('down')
            pg.press('down')
            pg.press('enter')
        except Exception:
            time.sleep(2)
            pass

def select_purchase_order_list():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/busy_purchase_order.png', confidence=0.9)
            pg.click(location)
            pg.press('down')
            pg.press('down')
            pg.press('enter')
        except Exception:
            time.sleep(2)
            pass

def select_mrfp_list():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/mrfp.png', confidence=0.9)
            pg.click(location)
            pg.press('down')
            pg.press('down')
            pg.press('enter')
        except Exception:
            time.sleep(2)
            pass

def select_salesorder_list():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/salesorder.png', confidence=0.9)
            pg.click(location)
            pg.press('down')
            pg.press('down')
            pg.press('enter')
        except Exception:
            time.sleep(2)
            pass
  
def select_stock_transfer_list():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/stock_transfer.png', confidence=0.9)
            pg.click(location)
            pg.press('down')
            pg.press('down')
            pg.press('enter')
        except Exception:
            time.sleep(2)
            pass

def select_stock_journal_list():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/stock_journal.png', confidence=0.9)
            pg.click(location)
            pg.press('down')
            pg.press('down')
            pg.press('enter')
        except Exception:
            time.sleep(2)
            pass

def select_production_list():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/production.png', confidence=0.9)
            pg.click(location)
            pg.press('down')
            pg.press('down')
            pg.press('enter')
        except Exception:
            time.sleep(2)
            pass

def list_format(report_type, start_date, end_date):
    busy_utils.find_img('busy/images/busy_list.png')
    time.sleep(1)
    
    #format name
    if report_type == "sales" or report_type == "sales_return":  
        pg.typewrite('new')
    if report_type == "material_received_from_party" or report_type == "material_issued_to_party":
        pg.typewrite('new')
    if report_type == "sales_order":
        pg.typewrite('order value')    
    
    pg.press('enter')

    pg.typewrite("a")
    pg.press("backspace")               #select branch
    time.sleep(0.3)
    pg.press('enter')

    pg.typewrite("a")
    pg.press("backspace")              #voucher series
    time.sleep(0.3)
    pg.press('enter')

    pg.typewrite("all")               #salesman range
    time.sleep(0.3)
    pg.press('enter')

    pg.typewrite(start_date)          #start date
    pg.press('enter')

    pg.typewrite(end_date)            #end date
    pg.press('enter')

    pg.typewrite('name')             #account to be shown
    pg.press('enter')

    pg.typewrite('both')            #report to be shown in
    pg.press('enter')

    pg.typewrite('name')           #item to be shown in 
    pg.press('enter')
    
    pg.typewrite('y')           #show material centre namne 
    pg.press('enter')

    pg.typewrite('y')           #show value of items 
    pg.press('enter')

    if report_type != "sales_order":
        pg.typewrite('n')           #show batch details 
        pg.press('enter')
    else:
        pass

    if report_type == "sales" or report_type == "sales_return":
        pg.typewrite('y')           #show party TIN/GSTIN no 
        pg.press('enter')
    if report_type == "material_received_from_party" or report_type == "material_issued_to_party" or report_type == "sales_order":
        pass

    pg.typewrite('n')           #show report notes in column 
    pg.press('enter')

    pg.press('enter')  

def purchase_list_format(start_date, end_date):
    busy_utils.find_img('busy/images/list_image.png')
    time.sleep(1)
    
    #format name
    pg.typewrite('new', interval=0.2)    
    pg.press('enter')

    pg.typewrite("a")
    pg.press("backspace")               #select branch
    time.sleep(0.3)
    pg.press('enter')

    pg.typewrite("a")
    pg.press("backspace")              #voucher series
    time.sleep(0.3)
    pg.press('enter')

    pg.typewrite("all")               #salesman range
    time.sleep(0.3)
    pg.press('enter')

    pg.typewrite(start_date,interval=0.3)          #start date
    pg.press('enter')

    pg.typewrite(end_date,interval=0.3)            #end date
    pg.press('enter')

    pg.typewrite('name')             #account to be shown
    pg.press('enter')

    pg.typewrite('both')            #report to be shown in
    pg.press('enter')

    pg.typewrite('name')           #item to be shown in 
    pg.press('enter')
    
    pg.typewrite('y')           #show material centre namne 
    pg.press('enter')

    pg.typewrite('y')           #show value of items 
    pg.press('enter')

    pg.typewrite('n')           #show batch details 
    pg.press('enter')

    pg.typewrite('y')           #show party TIN/GSTIN no 
    pg.press('enter')

    pg.typewrite('n')           #show report notes in column 
    pg.press('enter')

    
    pg.typewrite('n')           #show report notes in column 
    pg.press('enter')

def stock_list_format(report_type, start_date, end_date):
    busy_utils.find_img('busy/images/list_image.png')
    time.sleep(1)
    
    pg.typewrite('new')    
    pg.press('enter')

    pg.typewrite("a")
    pg.press("backspace")               #select branch
    time.sleep(0.3)
    pg.press('enter')

    pg.typewrite("a")
    pg.press("backspace")              #voucher series
    time.sleep(0.3)
    pg.press('enter')

    pg.typewrite(start_date)          #start date
    pg.press('enter')

    pg.typewrite(end_date)            #end date
    pg.press('enter')

    pg.typewrite('both')            #report to be shown in
    pg.press('enter')

    pg.typewrite('name')           #item to be shown in 
    pg.press('enter')
    
    if report_type != 'stock_transfer':
        pg.typewrite('y')           #show material centre namne 
        pg.press('enter')
    else:
        pass
    
    pg.typewrite('y')           #show value of items 
    pg.press('enter')

    pg.typewrite('n')           #show batch details 
    pg.press('enter')

    pg.typewrite('n')           #show report notes in column 
    pg.press('enter')

    pg.press('enter')

def transaction_report_selection(report):
    time.sleep(5)
    select_transaction()
    report()

#raw material
# purchase_order , purchase, purchase_return

def purchase_list_rm(report,start_date, end_date):
    if report == 'purchase':
        handle_purchase_formate(start_date=start_date, end_date=end_date)
    elif report == 'purchase_order':
        handle_purchase_order_format(start_date=start_date, end_date=end_date)
    elif report == 'purchase_return':
        handle_purchase_return_formate(start_date=start_date, end_date=end_date)

def handle_purchase_formate(start_date, end_date):
    time.sleep(2)
    pg.typewrite('New')
    time.sleep(1)
    pg.press('enter')

    time.sleep(1)
    pg.typewrite('<<-ALL->>',interval=0.3)
    time.sleep(1)
    pg.press("enter")

    time.sleep(1)
    pg.typewrite('<<-ALL->>',interval=0.3)
    time.sleep(1)
    pg.press("enter")

    time.sleep(1)
    pg.typewrite('<<-ALL->>',interval=0.3)
    time.sleep(1)
    pg.press("enter")


    pg.typewrite(start_date,interval=0.3)
    time.sleep(1)          #start date
    pg.press('enter')

    pg.typewrite(end_date,interval=0.3) 
    time.sleep(1)           #end date
    pg.press('enter')

    
    time.sleep(1)
    pg.typewrite('Name',interval=0.3)
    time.sleep(1)
    pg.press("enter")


        
    time.sleep(1)
    pg.typewrite('Name',interval=0.3)
    time.sleep(1)
    pg.press("enter")

    pg.typewrite('y')           #show value of items 
    pg.press('enter')
    
    pg.typewrite('y')           #show value of items 
    pg.press('enter')

        
    pg.typewrite('n')           #show value of items 
    pg.press('enter')
    
    pg.typewrite('y')           #show value of items 
    pg.press('enter')

    pg.typewrite('n')           #show value of items 
    pg.press('enter')

    time.sleep(1)
    pg.press('f2')

def handle_purchase_order_format(start_date, end_date):
    time.sleep(2)
    pg.typewrite('New')
    time.sleep(0.5)
    pg.press('enter')

    time.sleep(0.5)
    pg.typewrite('<<-ALL->>',interval=0.3)
    time.sleep(0.5)
    pg.press("enter")

    time.sleep(0.5)
    pg.typewrite('<<-ALL->>',interval=0.3)
    time.sleep(0.5)
    pg.press("enter")

    time.sleep(0.5)
    pg.typewrite('<<-ALL->>',interval=0.3)
    time.sleep(0.5)
    pg.press("enter")


    pg.typewrite(start_date,interval=0.3)
    time.sleep(0.5)          #start date
    pg.press('enter')

    pg.typewrite(end_date,interval=0.3) 
    time.sleep(0.5)           #end date
    pg.press('enter')


    time.sleep(0.5)
    pg.typewrite('Name',interval=0.3)
    time.sleep(0.5)
    pg.press("enter")

    time.sleep(0.5)
    pg.typewrite('Name',interval=0.3)
    time.sleep(0.5)
    pg.press("enter")

    time.sleep(0.5)
    pg.press('y')
    time.sleep(0.5)
    pg.press('enter')

    time.sleep(0.5)
    pg.press('y')
    time.sleep(0.5)
    pg.press('enter')

    time.sleep(0.5)
    pg.press('n')
    time.sleep(0.5)
    pg.press('enter')

    time.sleep(0.5)
    pg.press('f2')

def handle_purchase_return_formate(start_date, end_date):
    time.sleep(2)
    pg.typewrite('New')
    time.sleep(0.5)
    pg.press('enter')

    time.sleep(0.5)
    pg.typewrite('<<-ALL->>',interval=0.3)
    time.sleep(0.5)
    pg.press("enter")

    time.sleep(0.5)
    pg.typewrite('<<-ALL->>',interval=0.3)
    time.sleep(0.5)
    pg.press("enter")

    time.sleep(0.5)
    pg.typewrite('<<-ALL->>',interval=0.3)
    time.sleep(0.5)
    pg.press("enter")


    pg.typewrite(start_date,interval=0.3)
    time.sleep(0.5)          #start date
    pg.press('enter')

    pg.typewrite(end_date,interval=0.3) 
    time.sleep(0.5)           #end date
    pg.press('enter')


    time.sleep(0.5)
    pg.typewrite('Name',interval=0.3)
    time.sleep(0.5)
    pg.press("enter")

    time.sleep(0.5)
    pg.typewrite('Name',interval=0.3)
    time.sleep(0.5)
    pg.press("enter")


    time.sleep(0.5)
    pg.press('y')
    time.sleep(0.5)
    pg.press('enter')

    time.sleep(0.5)
    pg.press('y')
    time.sleep(0.5)
    pg.press('enter')

    time.sleep(0.5)
    pg.press('n')
    time.sleep(0.5)
    pg.press('enter')

    time.sleep(0.5)
    pg.press('y')
    time.sleep(0.5)
    pg.press('enter')

    time.sleep(0.5)
    pg.press('n')
    time.sleep(0.5)
    pg.press('enter')

    time.sleep(0.5)
    pg.press('f2')


#Stock

def stock_list_rm(report,start_date, end_date):
    if report =='stock_journal':
        handle_stock_journal_fromat(start_date=start_date, end_date=end_date)
    elif report == 'stock_transfer':
        handle_stock_transfer_format(start_date=start_date, end_date=end_date)
    elif report =='production':
        handle_production(start_date=start_date, end_date=end_date)

def handle_stock_transfer_format(start_date, end_date):
    busy_utils.find_img('busy/images/list_image.png')
    time.sleep(1)

    pg.typewrite('New')
    time.sleep(1)
    pg.press('enter')

    time.sleep(1)
    pg.typewrite('<<-ALL->>',interval=0.3)
    time.sleep(1)
    pg.press("enter")

    time.sleep(1)
    pg.typewrite('<<-ALL->>',interval=0.3)
    time.sleep(1)
    pg.press("enter")

    time.sleep(1)
    pg.typewrite('<<-ALL->>',interval=0.3)
    time.sleep(1)
    pg.press("enter")


    pg.typewrite(start_date,interval=0.3)
    time.sleep(1)          #start date
    pg.press('enter')

    pg.typewrite(end_date,interval=0.3) 
    time.sleep(1)           #end date
    pg.press('enter')

    
    time.sleep(1)
    pg.typewrite('Name',interval=0.3)
    time.sleep(1)
    pg.press("enter")

    time.sleep(0.5)
    pg.press('y')
    time.sleep(0.5)
    pg.press('enter')

    time.sleep(0.5)
    pg.press('n')
    time.sleep(0.5)
    pg.press('enter')


    time.sleep(0.5)
    pg.press('n')
    time.sleep(0.5)
    pg.press('enter')

    pg.press('f2')

def handle_stock_journal_fromat(start_date, end_date):
    busy_utils.find_img('busy/images/list_image.png')
    time.sleep(1)

    pg.typewrite('New')
    time.sleep(1)
    pg.press('enter')

    time.sleep(1)
    pg.typewrite('<<-ALL->>',interval=0.3)
    time.sleep(1)
    pg.press("enter")

    time.sleep(1)
    pg.typewrite('<<-ALL->>',interval=0.3)
    time.sleep(1)
    pg.press("enter")

    time.sleep(1)
    pg.typewrite('<<-ALL->>',interval=0.3)
    time.sleep(1)
    pg.press("enter")


    pg.typewrite(start_date,interval=0.3)
    time.sleep(1)          #start date
    pg.press('enter')

    pg.typewrite(end_date,interval=0.3) 
    time.sleep(1)           #end date
    pg.press('enter')

    
    time.sleep(1)
    pg.typewrite('Name',interval=0.3)
    time.sleep(1)
    pg.press("enter")

    time.sleep(0.5)
    pg.press('y')
    time.sleep(0.5)
    pg.press('enter')

    time.sleep(0.5)
    pg.press('y')
    time.sleep(0.5)
    pg.press('enter')

    time.sleep(0.5)
    pg.press('n')
    time.sleep(0.5)
    pg.press('enter')

    time.sleep(0.5)
    pg.press('n')
    time.sleep(0.5)
    pg.press('enter')

    pg.press('f2')

def handle_production(start_date, end_date):
    busy_utils.find_img('busy/images/list_image.png')
    time.sleep(1)

    pg.typewrite('New')
    time.sleep(1)
    pg.press('enter')

    time.sleep(1)
    pg.typewrite('<<-ALL->>',interval=0.3)
    time.sleep(1)
    pg.press("enter")

    time.sleep(1)
    pg.typewrite('<<-ALL->>',interval=0.3)
    time.sleep(1)
    pg.press("enter")

    time.sleep(1)
    pg.typewrite('<<-ALL->>',interval=0.3)
    time.sleep(1)
    pg.press("enter")


    pg.typewrite(start_date,interval=0.3)
    time.sleep(1)          #start date
    pg.press('enter')

    pg.typewrite(end_date,interval=0.3) 
    time.sleep(1)           #end date
    pg.press('enter')

    
    time.sleep(1)
    pg.typewrite('Name',interval=0.3)
    time.sleep(1)
    pg.press("enter")

    time.sleep(0.5)
    pg.press('y')
    time.sleep(0.5)
    pg.press('enter')

    time.sleep(0.5)
    pg.press('y')
    time.sleep(0.5)
    pg.press('enter')

    time.sleep(0.5)
    pg.press('n')
    time.sleep(0.5)
    pg.press('enter')

    time.sleep(0.5)
    pg.press('n')
    time.sleep(0.5)
    pg.press('enter')

    pg.press('f2')


#Matrial

def material_list_rm(report,start_date, end_date):
    if report =='material_received_from_party':
        handle_mrfp(start_date=start_date, end_date=end_date)
    elif report == 'material_issued_to_party':
        handle_mitp(start_date=start_date, end_date=end_date)

def handle_mrfp(start_date, end_date):
    busy_utils.find_img('busy/images/list_image.png')
    time.sleep(1)

    pg.typewrite('New')
    time.sleep(1)
    pg.press('enter')

    time.sleep(1)
    pg.typewrite('<<-ALL->>',interval=0.3)
    time.sleep(1)
    pg.press("enter")

    time.sleep(1)
    pg.typewrite('<<-ALL->>',interval=0.3)
    time.sleep(1)
    pg.press("enter")

    time.sleep(1)
    pg.typewrite('<<-ALL->>',interval=0.3)
    time.sleep(1)
    pg.press("enter")


    pg.typewrite(start_date,interval=0.3)
    time.sleep(1)          #start date
    pg.press('enter')

    pg.typewrite(end_date,interval=0.3) 
    time.sleep(1)           #end date
    pg.press('enter')

    
    time.sleep(1)
    pg.typewrite('Name',interval=0.3)
    time.sleep(1)
    pg.press("enter")
    
    time.sleep(1)
    pg.typewrite('Name',interval=0.3)
    time.sleep(1)
    pg.press("enter")

    pg.press('y')
    time.sleep(0.4)
    pg.press('enter')

    pg.press('y')
    time.sleep(0.4)
    pg.press('enter')

    pg.press('n')
    time.sleep(0.4)
    pg.press('enter')

    pg.press('n')
    time.sleep(0.4)
    pg.press('enter')

    pg.press('f2')

def handle_mitp(start_date, end_date):
    busy_utils.find_img('busy/images/list_image.png')
    time.sleep(1)

    pg.typewrite('New')
    time.sleep(1)
    pg.press('enter')

    time.sleep(1)
    pg.typewrite('<<-ALL->>',interval=0.3)
    time.sleep(1)
    pg.press("enter")

    time.sleep(1)
    pg.typewrite('<<-ALL->>',interval=0.3)
    time.sleep(1)
    pg.press("enter")

    time.sleep(1)
    pg.typewrite('<<-ALL->>',interval=0.3)
    time.sleep(1)
    pg.press("enter")


    pg.typewrite(start_date,interval=0.3)
    time.sleep(1)          #start date
    pg.press('enter')

    pg.typewrite(end_date,interval=0.3) 
    time.sleep(1)           #end date
    pg.press('enter')

    
    time.sleep(1)
    pg.typewrite('Name',interval=0.3)
    time.sleep(1)
    pg.press("enter")
    
    time.sleep(1)
    pg.typewrite('Name',interval=0.3)
    time.sleep(1)
    pg.press("enter")

    pg.press('y')
    time.sleep(0.4)
    pg.press('enter')

    pg.press('y')
    time.sleep(0.4)
    pg.press('enter')

    pg.press('n')
    time.sleep(0.4)
    pg.press('enter')

    pg.press('n')
    time.sleep(0.4)
    pg.press('enter')

    pg.press('f2')

