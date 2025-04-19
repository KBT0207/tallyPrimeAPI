import glob
import os
import time
from datetime import datetime, timedelta
import pyautogui as pg
from busy import busy_utils, export_busy_reports
from dotenv import load_dotenv
from logging_config import logger
from utils import email


load_dotenv('.env')


companies = ['comp0003']

# sales_dict = {'trans_list': [export_busy_reports.select_sales_list, 
#                                    export_busy_reports.select_salesreturn_list, 
#                                    export_busy_reports.select_salesorder_list,
#                                    ], 
#                 'reports': ['sales', 'sales_return', "sales_order",
#                                     ]}

material_dict = {'trans_list': [export_busy_reports.select_mrfp_list, 
                                export_busy_reports.select_mitp_list,
                                ], 
                'reports': ["material_received_from_party",
                            "material_issued_to_party",
                            ]}

stock_dict = {"trans_list": [export_busy_reports.select_stock_transfer_list, 
                             export_busy_reports.select_stock_journal_list, 
                             export_busy_reports.select_production_list, 
                             ], 
               "reports": ["stock_transfer", "stock_journal", "production", 
                           ]}

purchase_dict = {'trans_list': [export_busy_reports.select_purchase_list, 
                                export_busy_reports.select_purchase_order_list,
                                export_busy_reports.select_purchase_return_list,
                                ], 
                 'reports': ["purchase", "purchase_order", "purchase_return",
                            ]}



# def exporting_sales(start_date:str , end_date:str, filename:str, send_email:bool):

#     busy_utils.open_busy()
    
#     for comp in companies:

#         busy_utils.company_selection(comp_code = comp)
        
#         try:
#             busy_utils.busy_login(username= os.getenv('BUSY_USERNAME'),
#                             password= os.getenv('BUSY_PASSWORD'))
#             logger.info(f"Logged into Busy of {comp} successfully...")
#         except Exception as e:
#             logger.critical(f"Logging into Busy of {comp} Failed! : {e}")
        
#         for rep_func, report in zip(sales_dict['trans_list'], sales_dict['reports']):
#             if comp != "comp0005" and report == "sales_order" and rep_func == export_busy_reports.select_salesorder_list:
#                 continue
#             else:
#                 export_busy_reports.transaction_report_selection(report= rep_func)

#                 startdate_str = datetime.strptime(start_date, '%Y-%m-%d').strftime("%d-%m-%Y")
#                 todate_str = datetime.strptime(end_date, '%Y-%m-%d').strftime("%d-%m-%Y")
#                 try:
#                     export_busy_reports.list_format(report_type= report, 
#                                     start_date= startdate_str, 
#                                     end_date= todate_str)
#                     logger.info(f"Generated data for {comp} and {report} to export successfully...")
#                 except Exception as e:
#                     logger.critical(f"Data Generation for {comp} and {report} Failed! : {e}")

#                 try:
#                     busy_utils.export_format(report_type = report, company = comp, 
#                                             filename= f"{comp}_{report}_{filename}")
#                     logger.info(f"Exported data for {comp} and {report} successfully...")
#                 except Exception as e:
#                     logger.critical(f"Exporting Data for {comp} and {report} Failed! : {e}")
    
#                 try:
#                     busy_utils.return_to_busy_home(esc=3)
#                     time.sleep(5)

#                     logger.info(f"Report Generated for {comp} and {report} successfully and back to busy home...")
#                 except Exception as e:
#                     logger.critical(f"Failed to go back busy home! : {e}")

#         try:    
#             busy_utils.change_company()
#             time.sleep(5)
#             pg.press('enter')
#             logger.info(f"Successfully came to company page after {comp} page...")
#         except Exception as e:
#             logger.critical(f"Failed to go to company page! : {e}")

#     time.sleep(2)

#     busy_utils.find_img(img='busy/images/quit_at_login.png')
#     pg.click()
#     time.sleep(5)
#     pg.press('e')   
#     pg.press('enter')
#     logger.info("Quit Busy Successfully!")

#     if send_email:
#         receivers = ['shilpa@kaybeeexports.com', 'yerunkar.pradnya@kaybeeexports.com', 'sayali@kaybeeexports.com', 'hitesh@kaybeeexports.com']
#         cc = ['s.gaurav@kaybeeexports.com', 'danish@kaybeeexports.com']
#         attachment_path = glob.glob("E:\\automated_busy_downloads\\" + f"**\\*sales*{filename}.xlsx", recursive=True)

#         subj_sales = f"KB Companies ['Sales, Sales Voucher and Sales Order'] data of {todate_str}"
#         body_sales = f"Kindly find the attached 'Sales, Sales Voucher and Sales Order' data of {companies} from {startdate_str} to {todate_str}" 
#         attachment_path_sales = []
#         for file in attachment_path:
#             if 'sale' in file:
#                 attachment_path_sales.append(file) 
#         if len(attachment_path_sales) != 0:
#             try:
#                 email.email_send(reciever=receivers, cc = cc,
#                                 subject= subj_sales, 
#                                 contents= body_sales, 
#                                 attachemnts= attachment_path_sales)
#                 logger.info("Attachments (All Sales) emailed successfully... ")
#             except Exception as e:
#                 logger.critical(f"Failed to email the attachment for (All Sales)! : {e}")
#         else:
#             logger.critical("No data for (All Sales) exported today")


#         subj_sales_order = f"KBBIO Sales Order of {todate_str}"
#         attachment_path_sales_order = fr"E:\automated_busy_downloads\comp0005\sales_order\comp0005_sales_order_{filename}.xlsx"
#         body_sales_order = f"Kinldy find the Sales Order of {todate_str}"
#         if attachment_path_sales_order:
#             try:
#                 email.email_send(reciever="rajani@kaybeebio.com", cc = ["s.gaurav@kaybeeexports.com", "pranjal@kaybeebio.com"],
#                                 subject= subj_sales_order, 
#                                 contents= body_sales_order, 
#                                 attachemnts= attachment_path_sales_order)
#                 logger.info("Sales Order emailed successfully... ")
#             except Exception as e:
#                 logger.critical(f"Failed to email the attachment for Sales Order! : {e}")
#         else:
#             logger.critical("No data for Sales_Order exported today")
#     else:
#         logger.info(f"Busy Sales email not sent as per the argument given.")



def exporting_purchase(start_date:str, end_date:str, filename:str):

    busy_utils.open_busy()
    time.sleep(1)
    pg.press('enter')
    
    for comp in companies:

        busy_utils.company_selection(comp_code = comp)
        
        try:
            busy_utils.busy_login(username= os.getenv('BUSY_USERNAME'),
                            password= os.getenv('BUSY_PASSWORD'))
            logger.info(f"Logged into Busy of {comp} successfully...")
            time.sleep(1)
            pg.press('enter')
        except Exception as e:
            logger.critical(f"Logging into Busy of {comp} Failed! : {e}")
        for rep_func, report in zip(purchase_dict['trans_list'], purchase_dict['reports']):
            export_busy_reports.transaction_report_selection(report= rep_func)

            startdate_str = datetime.strptime(start_date, '%Y-%m-%d').strftime("%d-%m-%Y")
            todate_str = datetime.strptime(end_date, '%Y-%m-%d').strftime("%d-%m-%Y")
            try:
                export_busy_reports.purchase_list_rm(start_date= startdate_str, end_date= todate_str, report=report)
                logger.info(f"Generated data for {comp} and {report} to export successfully...")
            except Exception as e:
                logger.critical(f"Data Generation for {comp} and {report} Failed! : {e}")

            try:
                busy_utils.export_format(report_type = report, company = comp, 
                                        filename= f"{comp}_{report}_{filename}")
                logger.info(f"Exported data for {comp} and {report} successfully...")
            except Exception as e:
                logger.critical(f"Exporting Data for {comp} and {report} Failed! : {e}")

            try:
                busy_utils.return_to_busy_home(esc=3)
                time.sleep(5)

                logger.info(f"Report Generated for {comp} and {report} successfully and back to busy home...")
            except Exception as e:
                logger.critical(f"Failed to go back busy home! : {e}")

        try:    
            busy_utils.change_company()
            time.sleep(5)
            pg.press('enter')
            logger.info(f"Successfully came to company page after {comp} page...")
        except Exception as e:
            logger.critical(f"Failed to go to company page! : {e}")

    time.sleep(2)

    busy_utils.find_img(img='busy/images/quit_at_login.png')
    pg.click()
    time.sleep(5)
    pg.press('e')   
    pg.press('enter')
    logger.info("Quit Busy Successfully!")

    


def exporting_master_and_material(from_date:str, to_date:str, filename:str, send_email:bool):

    busy_utils.open_busy()
    
    for comp in companies:

        busy_utils.company_selection(comp_code = comp)
        
        try:
            busy_utils.busy_login(username= os.getenv('BUSY_USERNAME'),
                            password= os.getenv('BUSY_PASSWORD'))
            logger.info(f"Logged into Busy of {comp} successfully...")
        except Exception as e:
            logger.critical(f"Logging into Busy of {comp} Failed! : {e}")
            
        curr_date = datetime.today().strftime("%d-%b-%Y")

        for rep_func, report in zip(material_dict['trans_list'], material_dict['reports']):
        
            export_busy_reports.transaction_report_selection(report= rep_func)

            
            try:
                export_busy_reports.material_list_rm(report= report, 
                                start_date= from_date, 
                                end_date= to_date)
                logger.info(f"Generated data for {comp} and {report} to export successfully...")
            except Exception as e:
                logger.critical(f"Data Generation for {comp} and {report} Failed! : {e}")

            try:
                #curr_date = datetime.today().strftime("%d-%b-%Y")
                busy_utils.export_format(report_type = report, company = comp, 
                                        filename= f"{comp}_{report}_{filename}")
                logger.info(f"Exported data for {comp} and {report} successfully...")
            except Exception as e:
                logger.critical(f"Exporting Data for {comp} and {report} Failed! : {e}")

            try:    
                busy_utils.return_to_busy_home(esc=3)
                time.sleep(3)

                logger.info(f"Report Generated for {comp} and {report} successfully and back to busy home...")
            except Exception as e:
                logger.critical(f"Failed to go back busy home! : {e}")

        try:
            time.sleep(4)
            export_busy_reports.select_masters()
            export_busy_reports.select_accounts()
            busy_utils.export_format(report_type= "master_accounts", 
                                     company= comp, 
                                     filename=f"{comp}_master_accounts_{filename}")
            
            busy_utils.return_to_busy_home(esc=6)
            time.sleep(5)
            logger.info(f"Master Accounts for {comp} generated successfully and back to busy home...")
        except Exception as e:
            logger.critical(f"Failed to go back busy home! : {e}")
      
        try:
            export_busy_reports.select_masters()
            export_busy_reports.select_items()
            busy_utils.export_format(report_type= "items", 
                                            company= comp, 
                                            filename=f"{comp}_items_{filename}")
                    
            logger.info(f"Items Data for {comp} generated successfully and back to busy home...")
            busy_utils.return_to_busy_home(esc=5)
        except Exception as e:
            logger.critical(f"Failed to go back busy home! : {e}")

        try:    
            busy_utils.change_company()
            time.sleep(5)
            pg.press('enter')
            logger.info(f"Successfully came to company page after {comp} page...")
        except Exception as e:
            logger.critical(f"Failed to go to company page! : {e}")

    time.sleep(2)

    busy_utils.find_img(img='busy/images/quit_at_login.png')
    pg.click()
    time.sleep(5)
    pg.press('e')
    pg.press('enter')
    logger.info("Quit Busy Successfully!")

    # if send_email:
    #     receivers = ['shivprasad@kaybeebio.com', 'danish@kaybeeexports.com', 'rajani@kaybeebio.com']
    #     #receivers = ['s.gaurav@kaybeeexports.com']
    #     body_material = f"Kindly find the attached MITP & MRFP data of {companies} from {from_date} to {to_date}"
        
    #     attachment_path = glob.glob(f"E:\\automated_busy_downloads\\**\\*{filename}.xlsx", recursive=True)

    #     subj_material = f"KB Companies ['MITP & MRFP'] data of MTD of {datetime.today().strftime("%B")}"
    #     attachment_path_material = []
    #     for file in attachment_path:
    #         if 'material' in file:
    #             attachment_path_material.append(file) 
    #     if len(attachment_path_material) != 0:
    #         try:
    #             email.email_send(reciever=receivers, cc = "s.gaurav@kaybeeexports.com", 
    #                             subject= subj_material, 
    #                             contents= body_material, 
    #                             attachemnts= attachment_path_material)
    #             logger.info("Attachments of MITP & MRFP emailed successfully... ")
    #         except Exception as e:
    #             logger.critical(f"Failed to email the attachment for (MITP & MRFP)! : {e}")

    #     else:
    #         logger.critical("No data for MITP & MRFP exported today")

    #     try:
    #         subj_masters = f"Masters of KBBIO ({to_date})"
    #         body_masters = f"Kindly find the attached Masters data of KBBIO of {to_date}"
    #         masters_file = fr"E:\automated_busy_downloads\comp0005\master_accounts\comp0005_master_accounts_{filename}.xlsx"
    #         email.email_send(reciever= ['rajani@kaybeebio.com', 'pranjal@kaybeebio.com'], 
    #                         cc = ["s.gaurav@kaybeeexports.com", 'danish@kaybeeexports.com'], 
    #                         subject= subj_masters, contents= body_masters, attachemnts= masters_file)
    #         logger.info("KBBIO Masters Data emailed successfully... ")
    #     except Exception as e:
    #         logger.critical(f"Failed to email the masters data! : {e}")
        
    #     else:
    #         logger.info(f'Emails not done as per the argument given: {send_email}')



def exporting_stock(start_date:str , end_date:str, filename:str):

    busy_utils.open_busy()
    
    for comp in companies:

        busy_utils.company_selection(comp_code = comp)
        # change financial year comming

        
        try:
            busy_utils.busy_login(username= os.getenv('BUSY_USERNAME'),
                            password= os.getenv('BUSY_PASSWORD'))
            logger.info(f"Logged into Busy of {comp} successfully...")
            pg.press('enter')
        except Exception as e:
            logger.critical(f"Logging into Busy of {comp} Failed! : {e}")
        
        for rep_func, report in zip(stock_dict['trans_list'], stock_dict['reports']):
            export_busy_reports.transaction_report_selection(report= rep_func)

            startdate_str = datetime.strptime(start_date, '%Y-%m-%d').strftime("%d-%m-%Y")
            todate_str = datetime.strptime(end_date, '%Y-%m-%d').strftime("%d-%m-%Y")
            try:
                export_busy_reports.stock_list_rm(report= report, 
                                start_date= startdate_str, 
                                end_date= todate_str)
                logger.info(f"Generated data for {comp} and {report} to export successfully...")
            except Exception as e:
                logger.critical(f"Data Generation for {comp} and {report} Failed! : {e}")

            try:
                busy_utils.export_format(report_type = report, company = comp, 
                                        filename= f"{comp}_{report}_{filename}")
                logger.info(f"Exported data for {comp} and {report} successfully...")
            except Exception as e:
                logger.critical(f"Exporting Data for {comp} and {report} Failed! : {e}")

            try:
                busy_utils.return_to_busy_home(esc=3)
                time.sleep(5)

                logger.info(f"Report Generated for {comp} and {report} successfully and back to busy home...")
            except Exception as e:
                logger.critical(f"Failed to go back busy home! : {e}")

        try:    
            busy_utils.change_company()
            time.sleep(5)
            pg.press('enter')
            logger.info(f"Successfully came to company page after {comp} page...")
        except Exception as e:
            logger.critical(f"Failed to go to company page! : {e}")

    time.sleep(2)

    busy_utils.find_img(img='busy/images/quit_at_login.png')
    pg.click()
    time.sleep(5)
    pg.press('e')   
    pg.press('enter')
    logger.info("Quit Busy Successfully!")

    # if send_email:
    #     receivers = ['shilpa@kaybeeexports.com', 'yerunkar.pradnya@kaybeeexports.com', 'sayali@kaybeeexports.com', 'hitesh@kaybeeexports.com']
    #     cc = ['s.gaurav@kaybeeexports.com', 'danish@kaybeeexports.com']
    #     attachment_path = glob.glob("E:\\automated_busy_downloads\\" + f"**\\*sales*{filename}.xlsx", recursive=True)

    #     subj_sales = f"KB Companies ['Sales, Sales Voucher and Sales Order'] data of {todate_str}"
    #     body_sales = f"Kindly find the attached 'Sales, Sales Voucher and Sales Order' data of {companies} from {startdate_str} to {todate_str}" 
    #     attachment_path_sales = []
    #     for file in attachment_path:
    #         if 'sale' in file:
    #             attachment_path_sales.append(file) 
    #     if len(attachment_path_sales) != 0:
    #         try:
    #             email.email_send(reciever=receivers, cc = cc,
    #                             subject= subj_sales, 
    #                             contents= body_sales, 
    #                             attachemnts= attachment_path_sales)
    #             logger.info("Attachments (All Sales) emailed successfully... ")
    #         except Exception as e:
    #             logger.critical(f"Failed to email the attachment for (All Sales)! : {e}")
    #     else:
    #         logger.critical("No data for (All Sales) exported today")


    #     subj_sales_order = f"KBBIO Sales Order of {todate_str}"
    #     attachment_path_sales_order = fr"E:\automated_busy_downloads\comp0005\sales_order\comp0005_sales_order_{filename}.xlsx"
    #     body_sales_order = f"Kinldy find the Sales Order of {todate_str}"
    #     if attachment_path_sales_order:
    #         try:
    #             email.email_send(reciever="rajani@kaybeebio.com", cc = ["s.gaurav@kaybeeexports.com", "pranjal@kaybeebio.com"],
    #                             subject= subj_sales_order, 
    #                             contents= body_sales_order, 
    #                             attachemnts= attachment_path_sales_order)
    #             logger.info("Sales Order emailed successfully... ")
    #         except Exception as e:
    #             logger.critical(f"Failed to email the attachment for Sales Order! : {e}")
    #     else:
    #         logger.critical("No data for Sales_Order exported today")
    # else:
    #     logger.info(f"Busy Sales email not sent as per the argument given.")


