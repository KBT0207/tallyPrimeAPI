"""This module contain functions that will used as helper/common functions in the report modules 
"""
import calendar
from datetime import datetime
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



from database.models.busy_models.busy_accounts import (BusyAccounts100x,
                                                       BusyAccountsAgri,
                                                       BusyAccountsGreenEra,
                                                       BusyAccountsKBBIO,
                                                       BusyAccountsNewAge)
from database.models.busy_models.busy_items import (BusyItems100x,
                                                    BusyItemsAgri,
                                                    BusyItemsGreenEra,
                                                    BusyItemsKBBIO,
                                                    BusyItemsNewAge)
from database.models.busy_models.busy_pricing import BusyPricingKBBIO
from database.models.busy_models.busy_reports import (MITPKBBIO, MRFPKBBIO,
                                                      SalesKBBIO, SalesOrderKBBIO, SalesReturnKBBIO, 
                                                      Production, StockJournal, StockTransfer, PurchaseKBBIO, PurchaseReturnKBBIO )
from database.models.kbe_models.tally_kbe_models import (
    TallyAccounts, TallyJournal,
    TallyPayment, TallyPurchase, TallyPurchaseReturn, TallyReceipts,
    TallySales, TallySalesReturn,TallySalesDetailed, TallySalesReturnDetailed)

from database.models.kbe_models.export_models import KBEOutstanding, ExchangeRate

from database.models.trackwick.trackwick_models import (TrackwickEmployees, TrackwickSubDealerLiquidationTasks, 
                                                        TrackwickFarmerLiquidationTasks, TrackwickDealerCollectionTasks, 
                                                        TrackwickDealerSalesOrderTasks, TrackwickFeedbackTasks, 
                                                        TrackwickCarTravelExpenses, TrackwickBikeTravelExpenses, 
                                                        TrackwickOtherTravelExpenses, 
                                                        )


# from database.models.busy_models.busy_accounts_rm import (BusyAccountsKBBIORM)
from database.models.busy_models.busy_reports_rm import (RMMITPKBBIO,RMMRFPKBBIO,RMProduction,RMStockJournal,RMStockTransfer,RMPurchaseReturnKBBIO,RMPurchaseKBBIO,RMPurchaseOrder)
from database.models.busy_models.busy_accounts_rm import BusyAccountsKBBIORM
from database.models.busy_models.busy_item_rm import BusyItemsKBBIORM


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




busy_tables = {'busy_sales': SalesKBBIO, 'busy_sales_order': SalesOrderKBBIO, 'busy_sales_return': SalesReturnKBBIO, 
               "busy_mitp": MITPKBBIO, "busy_mrfp": MRFPKBBIO, 
                "busy_acc_kbbio": BusyAccountsKBBIO, "busy_acc_100x": BusyAccounts100x, "busy_acc_agri": BusyAccountsAgri,
                "busy_acc_greenera": BusyAccountsGreenEra, "busy_acc_newage": BusyAccountsNewAge, 
                "busy_items_kbbio": BusyItemsKBBIO, "busy_items_100x": BusyItems100x,  "busy_items_agri": BusyItemsAgri,
                "busy_items_greenera": BusyItemsGreenEra, "busy_items_newage": BusyItemsNewAge, 
                "production": Production, "busy_stock_transfer": StockTransfer, "busy_stock_journal": StockJournal, 
                "busy_purchase": PurchaseKBBIO, "busy_purchase_return": PurchaseReturnKBBIO, 
            }

busyrm_tables = {
    "busyrm_purchase": RMPurchaseKBBIO, 'busyrm_purchase_order':RMPurchaseOrder,
    "busyrm_purchase_return":RMPurchaseReturnKBBIO,

    'busyrm_stock_journal':RMStockJournal, 'busyrm_stock_transfer':RMStockTransfer,
    'busyrm_production':RMProduction,

    'busyrm_mrfp':RMMRFPKBBIO, 'busyrm_mitp':RMMITPKBBIO,

    "busyrm_acc":BusyAccountsKBBIORM,
    "busyrm_items":BusyItemsKBBIORM,


}

tally_tables = {"tally_sales": TallySales, "tally_sales_return": TallySalesReturn, 
                "tally_purchase": TallyPurchase, "tally_purchase_return": TallyPurchaseReturn, 
                "tally_payments": TallyPayment, "tally_receipts": TallyReceipts, "tally_journal": TallyJournal, 
                "tally_accounts": TallyAccounts,"tally_sales_detailed":TallySalesDetailed,'tally_sales_return_detailed':TallySalesReturnDetailed
                }

kbe_tables = {"outstanding_balance": KBEOutstanding, "exchange_rate": ExchangeRate,}

# other_tables = {"busy_pricing_kbbio": BusyPricingKBBIO, "test_table": TestTable,
#                }

trackwick_tables = {"trackwick_employees": TrackwickEmployees, 
                    'trackwick_sub_dealer_liquidation_tasks': TrackwickSubDealerLiquidationTasks, 
                    'trackwick_farmer_liquidation_tasks': TrackwickFarmerLiquidationTasks, 
                    'trackwick_dealer_collection_tasks': TrackwickDealerCollectionTasks, 
                    'trackwick_dealer_sales_order_tasks': TrackwickDealerSalesOrderTasks, 
                    'trackwick_feedback_tasks': TrackwickFeedbackTasks, 
                    "trackwick_car_travel_expense": TrackwickCarTravelExpenses, 
                    "trackwick_bike_travel_expense": TrackwickBikeTravelExpenses, 
                    "trackwick_other_travel_expense": TrackwickOtherTravelExpenses, 
                    }


tables = {**tally_tables,**busyrm_tables}


tally_reports = {
                's': 'sales', 
                'e': 'sales-return',
                'p': "purchase" , 
                'd': 'purchase-return',
                'y': "payments",
                'r': 'receipts', 'j': 'journal',
                }


tally_reports_detailed = {
                's': 'sales-detailed', 
                'e': 'sales-return-detailed',
                }
        

volume_discount_scheme = {}


tally_comp_codes = {
                    10001: "Pune",
                    10002: "Pune" , 
                    10003: "Indore", 
                    10004: "Jejuri", 
                    10005: "Nashik", 
                    10007: "Hubli",                     
                    10008: "Raipur", 
                    10009: "Vijaywada", 
                    10010: "Ahmedabad",
                    10011: "Hyderabad", 
                    10012: "Lucknow", 
                    10014: "NA Phaltan", 
                    10016: "Karnal", 
                    10017: "GE Phaltan", 
                    10018: "100x Phaltan", 
                    10019: "Jaipur", 
                    10020: "Khorda", 
                    10021: "AS Phaltan", 
                    10022: "Bhatinda",
                    10023: "NA Hubli", 
                    # 20000: "Phaltan",  
                    20001: "Phaltan", 
                    # 91820: "Phaltan",
                    }


acc_comp_codes = {
                    10001: "Pune",
                    10002: "Baner" , 
                    10003: "Indore",
                    10004: "Jejuri",
                    10005: "Nashik", 
                    10007: "Hubli",                     
                    10008: "Raipur", 
                    10009: "Vijaywada", 
                    10010: "Ahmedabad", 
                    10011: "Hyderabad", 
                    10012: "Lucknow", 
                    10014: "NA Phaltan", 
                    10016: "Karnal", 
                    10017: "GE Phaltan", 
                    10018: "100x Phaltan",
                    10019: "Jaipur", 
                    10020: "Khorda", 
                    10021: "AS Phaltan", 
                    10022: "Bhatinda",
                    10023: "NA Hubli", 
                    20001: "Phaltan", 
                    }


balance_comp_codes = {
                    10001: "Pune",
                    # 10002: "Baner" , 
                    10003: "Indore",
                    # 10004: "Jejuri",
                    10005: "Nashik", 
                    10007: "Hubli",                     
                    10008: "Raipur", 
                    10009: "Vijaywada", 
                    10010: "Ahmedabad", 
                    10011: "Hyderabad", 
                    10012: "Lucknow", 
                    10014: "NA Phaltan", 
                    10016: "Karnal", 
                    10017: "GE Phaltan", 
                    # 10018: "100x Phaltan",
                    10019: "Jaipur", 
                    10020: "Khorda", 
                    10021: "AS Phaltan", 
                    10022: "Bhatinda",
                    10023: "NA Hubli", 
                    20001: "Phaltan", 
                    }


kbe_outstanding_comp_codes = {
                    10000: "KBFruit",
                    10001: "Frex",
                    10003: "Orbit",
                    10004: "KBAgro",
                    10005: "KBEIPL", 
                    12022: "KBE",                     
                    92021: "KBVeg", 
                            }


receivables_comp_codes = {
                    # 10001: "Pune",
                    10002: "Baner" , 
                    10003: "Indore",
                    # 10004: "Jejuri",
                    10005: "Nashik", 
                    10007: "Hubli",                     
                    10008: "Raipur", 
                    10009: "Vijaywada", 
                    10010: "Ahmedabad", 
                    10011: "Hyderabad", 
                    10012: "Lucknow", 
                    10014: "NA Phaltan", 
                    10016: "Karnal", 
                    10017: "GE Phaltan", 
                    # 10018: "100x Phaltan",
                    10019: "Jaipur", 
                    10020: "Khorda", 
                    10021: "AS Phaltan", 
                    10022: "Bhatinda",
                    10023: "NA Hubli", 
                    20001: "Phaltan", 
                    }


company_dict_kaybee_exports = {
    # 'KAY BEE EXPORTS INTERNATIONAL PVT LTD (Phaltan NA) - (from 1-Apr-23)':'Phaltan KBEIPL',
    # 'Kay Bee Exports - Agri Division Phaltan 21-22':'Phaltan NA KBE',
    # 'KAY BEE EXPORTS (PHALTAN) FY21-22':'Phaltan A KBE',
    # "KAY BEE EXPORTS INTERNATIONAL PVT LTD (Thane) - (from 2024)": "Thane KBEIPL",
    # "Fab Fresh Fruits": "Thane Fab Fresh",
    # "KAY BEE EXPORTS INTERNATIONAL PVT LTD (Nagar NA) - (from 1-Apr-23)": "Nagar KBEIPL",
    # "KAY BEE EXPORTS INTERNATIONAL PVT LTD -Vashi": "Vashi KBEIPL",
    # "KAY BEE EXPORTS INTERNATIONAL PVT LTD (Gujarat)": "Gujarat KBEIPL",
    # "KAY BEE EXPORTS INTERNATIONAL PVT LTD (CARGO)": "Cargo KBEIPL",
    # "Kay Bee Exports - Thane (From Apr-24)": "Thane KBE",
    # "Kay Bee Exports - Vashi FY 2022-23 & 23-24": "Vashi KBE",
    # "Kay Bee Exports - Nagar Non Agri Divsion - FY 2021-22": "Nagar NA KBE",
    # "Kay Bee Exports - Agri Div. Nagar - FY2022-23 & 2023-24": "Nagar A KBE",
    # "Kay Bee Exports - Gujarat - FY2021-22": "Gujarat KBE",
    # "KAY BEE EXPORTS-MP FY 2021-22": "MP KBE",
    # "KAY BEE EXPORTS (JDS)": "JDS KBE",
    # "KAY BEE CARGO": "Cargo KBE",
    # "Orbit Exports (MH) from Apr-24": "Thane Orbit",
    # "Orbit Exports (Gujarat)": "Gujarat Orbit",    
    # "Frexotic Foods (From Apr-24)": "Thane Frexotic",
    
    "Kay Bee Agro International Pvt Ltd (GJ)": "Gujarat KBAIPL",
    "Kay Bee Agro International Pvt Ltd (MH)": "Thane KBAIPL",
    "Kay Bee Agro International Pvt Ltd (MP)": "MP KBAIPL",
    "Kay Bee Farm Management Services Pvt Ltd": "MP KBFMSPL",
    "Fruit & Veg Private Limited": "MP F&VPL",
    "KAY BEE FRESH VEG & FRUIT PVT LTD": "MP KBFV&FPL",
    "Kay Bee Veg Pvt Ltd": "MP KBVPL",
    "Kay Bee Agro Farms Pvt Ltd - (From 1-Apr-2016)": "Thane KBAFPL",
    "Kay Bee veg Ltd - FY 2020-21": "UK KB Veg",
    "KAY BEE FRUITS INC": "USA KB Fruits",
    "Aamrica Fresh Private Limited": "Thane Aamrica",
    "Freshnova Private Limited": "Thane Freshnova",
    "Kay Bee Fresh LLP": "Thane KB Fresh",
    "Perfect Produce Partners": "Thane Perfect Produce",
    "Indifuit": "Thane Indifruit",
    }

fcy_company = {
    "Freshnova Pvt Ltd (FCY)": "FCY Freshnova",
    "Frexotic Foods (FCY)": "FCY Frexotic",
    "Kay Bee Exports (FCY) FROM 20-21": "FCY KBE",
    "KAY BEE EXPORTS INTERNATIONAL PVT LTD (FCY)": "FCY KBEIPL",
    "Orbit Exports (FCY)": "FCY Orbit",
    "Kay Bee Agro International Pvt Ltd (FCY)": "FCY KBAIPL",
    'Freshnova Pvt Ltd (FCY)':'FCY Freshnova',
}


all_columner_comp = {
    # "Frexotic Foods (FCY)": "FCY Frexotic",
    # "Kay Bee Exports (FCY) FROM 20-21": "FCY KBE",
    # "KAY BEE EXPORTS INTERNATIONAL PVT LTD (FCY)": "FCY KBEIPL",
    # "Orbit Exports (FCY)": "FCY Orbit",
    # "Kay Bee Agro International Pvt Ltd (FCY)": "FCY KBAIPL",
    # "Kay Bee veg Ltd - FY 2020-21": "UK KB Veg",
    # 'Freshnova Pvt Ltd (FCY)':'FCY Freshnova',
    
    # 'KAY BEE EXPORTS INTERNATIONAL PVT LTD (Phaltan NA) - (from 1-Apr-23)':'Phaltan KBEIPL',
    # 'Kay Bee Exports - Agri Division Phaltan 21-22':'Phaltan NA KBE',
    # 'KAY BEE EXPORTS (PHALTAN) FY21-22':'Phaltan A KBE',

    "KAY BEE EXPORTS INTERNATIONAL PVT LTD (Thane) - (from 2024)": "Thane KBEIPL",
    "Fab Fresh Fruits": "Thane Fab Fresh",
    "KAY BEE EXPORTS INTERNATIONAL PVT LTD (Nagar NA) - (from 1-Apr-23)": "Nagar KBEIPL",
    "KAY BEE EXPORTS INTERNATIONAL PVT LTD -Vashi": "Vashi KBEIPL",
    "KAY BEE EXPORTS INTERNATIONAL PVT LTD (Gujarat)": "Gujarat KBEIPL",
    "KAY BEE EXPORTS INTERNATIONAL PVT LTD (CARGO)": "Cargo KBEIPL",
    "Kay Bee Exports - Thane (From Apr-24)": "Thane KBE",
    "Kay Bee Exports - Vashi FY 2022-23 & 23-24": "Vashi KBE",
    "Kay Bee Exports - Nagar Non Agri Divsion - FY 2021-22": "Nagar NA KBE",
    "Kay Bee Exports - Agri Div. Nagar - FY2022-23 & 2023-24": "Nagar A KBE",
    "Kay Bee Exports - Gujarat - FY2021-22": "Gujarat KBE",

    # "KAY BEE EXPORTS-MP FY 2021-22": "MP KBE",
    # "KAY BEE EXPORTS (JDS)": "JDS KBE",
    # "KAY BEE CARGO": "Cargo KBE",
    # "Orbit Exports (MH) from Apr-24": "Thane Orbit",
    # "Orbit Exports (Gujarat)": "Gujarat Orbit",    
    # "Frexotic Foods (From Apr-24)": "Thane Frexotic",
    # "Kay Bee Agro International Pvt Ltd (GJ)": "Gujarat KBAIPL",
    # "Kay Bee Agro International Pvt Ltd (MH)": "Thane KBAIPL",
    # "Kay Bee Agro International Pvt Ltd (MP)": "MP KBAIPL",
    # "Kay Bee Farm Management Services Pvt Ltd": "MP KBFMSPL",
    # "Fruit & Veg Private Limited": "MP F&VPL",
    # "KAY BEE FRESH VEG & FRUIT PVT LTD": "MP KBFV&FPL",
    # "Kay Bee Veg Pvt Ltd": "MP KBVPL",
    # "Kay Bee Agro Farms Pvt Ltd - (From 1-Apr-2016)": "Thane KBAFPL",
    # "Kay Bee veg Ltd - FY 2020-21": "UK KB Veg",
    # "KAY BEE FRUITS INC": "USA KB Fruits",
    # "Aamrica Fresh Private Limited": "Thane Aamrica",
    # "Freshnova Private Limited": "Thane Freshnova",
    # "Kay Bee Fresh LLP": "Thane KB Fresh",
    # "Perfect Produce Partners": "Thane Perfect Produce",
    # "Indifuit": "Thane Indifruit",
}

fcy_company = {
    "Frexotic Foods (FCY)": "FCY Frexotic",
    "Kay Bee Exports (FCY) FROM 20-21": "FCY KBE",
    "KAY BEE EXPORTS INTERNATIONAL PVT LTD (FCY)": "FCY KBEIPL",
    "Orbit Exports (FCY)": "FCY Orbit",
    "Kay Bee Agro International Pvt Ltd (FCY)": "FCY KBAIPL",
}


all_columner_comp = {
    "Frexotic Foods (FCY)": "FCY Frexotic",
    "Kay Bee Exports (FCY) FROM 20-21": "FCY KBE",
    "KAY BEE EXPORTS INTERNATIONAL PVT LTD (FCY)": "FCY KBEIPL",
    "Orbit Exports (FCY)": "FCY Orbit",
    "Kay Bee Agro International Pvt Ltd (FCY)": "FCY KBAIPL",
    "Kay Bee veg Ltd - FY 2020-21": "UK KB Veg",
    
    'KAY BEE EXPORTS INTERNATIONAL PVT LTD (Phaltan NA) - (from 1-Apr-23)':'Phaltan KBEIPL',
    'Kay Bee Exports - Agri Division Phaltan 21-22':'Phaltan NA KBE',
    'KAY BEE EXPORTS (PHALTAN) FY21-22':'Phaltan A KBE',
    "KAY BEE EXPORTS INTERNATIONAL PVT LTD (Thane) - (from 2024)": "Thane KBEIPL",
    "Fab Fresh Fruits": "Thane Fab Fresh",
    "KAY BEE EXPORTS INTERNATIONAL PVT LTD (Nagar NA) - (from 1-Apr-23)": "Nagar KBEIPL",
    "KAY BEE EXPORTS INTERNATIONAL PVT LTD -Vashi": "Vashi KBEIPL",
    "KAY BEE EXPORTS INTERNATIONAL PVT LTD (Gujarat)": "Gujarat KBEIPL",
    "KAY BEE EXPORTS INTERNATIONAL PVT LTD (CARGO)": "Cargo KBEIPL",
    "Kay Bee Exports - Thane (From Apr-24)": "Thane KBE",
    "Kay Bee Exports - Vashi FY 2022-23 & 23-24": "Vashi KBE",
    "Kay Bee Exports - Nagar Non Agri Divsion - FY 2021-22": "Nagar NA KBE",
    "Kay Bee Exports - Agri Div. Nagar - FY2022-23 & 2023-24": "Nagar A KBE",
    "Kay Bee Exports - Gujarat - FY2021-22": "Gujarat KBE",
    "KAY BEE EXPORTS-MP FY 2021-22": "MP KBE",
    "KAY BEE EXPORTS (JDS)": "JDS KBE",
    "KAY BEE CARGO": "Cargo KBE",
    "Orbit Exports (MH) from Apr-24": "Thane Orbit",
    "Orbit Exports (Gujarat)": "Gujarat Orbit",    
    "Frexotic Foods (From Apr-24)": "Thane Frexotic",
    
    "Kay Bee Agro International Pvt Ltd (GJ)": "Gujarat KBAIPL",
    "Kay Bee Agro International Pvt Ltd (MH)": "Thane KBAIPL",
    "Kay Bee Agro International Pvt Ltd (MP)": "MP KBAIPL",
    "Kay Bee Farm Management Services Pvt Ltd": "MP KBFMSPL",
    "Fruit & Veg Private Limited": "MP F&VPL",
    "KAY BEE FRESH VEG & FRUIT PVT LTD": "MP KBFV&FPL",
    "Kay Bee Veg Pvt Ltd": "MP KBVPL",
    "Kay Bee Agro Farms Pvt Ltd - (From 1-Apr-2016)": "Thane KBAFPL",
    "Kay Bee veg Ltd - FY 2020-21": "UK KB Veg",
    "KAY BEE FRUITS INC": "USA KB Fruits",
    "Aamrica Fresh Private Limited": "Thane Aamrica",
    "Freshnova Private Limited": "Thane Fresh Nova",
    "Kay Bee Fresh LLP": "Thane KB Fresh",
    "Perfect Produce Partners": "Thane Perfect Produce",
    "Indifuit": "Thane Indifruit",
}

kaybee_exports_currency = {
    'Phaltan KBEIPL':'INR',
    'Phaltan NA KBE':'INR',
    'Phaltan A KBE': "INR",
    "Thane Fab Fresh": "INR",
    "Thane KBEIPL": "INR",
    "Nagar KBEIPL": "INR",
    "Vashi KBEIPL": "INR",
    "Gujarat KBEIPL": "INR",
    "Cargo KBEIPL": "INR",
    "Thane KBE": "INR",
    "Vashi KBE": "INR",
    "Nagar NA KBE": "INR",
    "Nagar A KBE": "INR",
    "Gujarat KBE": "INR",
    "MP KBE": "INR",
    "JDS KBE": "INR",
    "Cargo KBE": "INR",
    "Thane Orbit": "INR",
    "Gujarat Orbit": "INR",
    "Thane Frexotic": "INR",
    "Gujarat KBAIPL": "INR",
    "Thane KBAIPL": "INR",
    "MP KBAIPL": "INR",
    "MP KBFMSPL": "INR",
    "MP F&VPL": "INR",
    "MP KBFV&FPL": "INR",
    "MP KBVPL": "INR",
    "Thane KBAFPL": "INR",
    "UK KB Veg": "GBP",
    "USA KB Fruits": "USD",
    "Thane Aamrica": "INR",
    "Thane Freshnova": "INR",
    "Thane KB Fresh": "INR",
    "Thane Perfect Produce": "INR",
    "Thane Indifruit": "INR",
}
