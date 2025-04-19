from sqlalchemy import insert, distinct, and_, case, func, cast, DECIMAL, select, Numeric, Table, text, MetaData
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
import numpy as np
import datetime as dt
import os
from xlwings import view
from sqlalchemy.orm import scoped_session, sessionmaker
from Database.db_crud import DatabaseCrud
from logging_config import logger
# from utils.email import email_send
from Database.models.busy_models.busy_pricing import BusyPricingKBBIO
from Database.models.busy_models.busy_accounts import (BusyAccounts100x, BusyAccountsAgri, 
                                                    BusyAccountsGreenEra, BusyAccountsKBBIO,
                                                    BusyAccountsNewAge)
from Database.models.busy_models.busy_reports import (SalesKBBIO, SalesOrderKBBIO, SalesReturnKBBIO, MITPKBBIO, MRFPKBBIO)
from Database.models.tally_models.tally_report_models import (TallyAccounts, TallyOutstandingBalance, 
                                                              TallySales, TallySalesReturn, TallyJournal, 
                                                              TallyPayment, TallyPurchase, TallyPurchaseReturn ,
                                                              TallyReceipts, DebtorsBalance
                                                              )



class SalesPriceValidation:

    def __init__(self, db_connector):
        self.db_connector = db_connector
        self.Session = scoped_session(sessionmaker(bind=self.db_connector.engine, autoflush=False))


    def sales_price_validation(self, from_date: str, to_date: str, exceptions: list = None) -> pd.DataFrame:
        """This method queries the database to provide busy sales price validation report in a dataframe.

        Args:
            from_date (str): The date from which busy sales needed to be validated from.
            to_date (str): The date till which busy sales needed to be validated.
            exceptions (list, optional): Takes in Sales Voucher Number which you want to be excluded from the report. Defaults to None.

        Returns:
            pd.DataFrame: Dataframe includes relevant columns of 'busy_sales' along with Price List column. 
        """
        join_query = self.Session.query(SalesKBBIO, BusyPricingKBBIO).outerjoin(
            BusyPricingKBBIO, and_(
                SalesKBBIO.party_type == BusyPricingKBBIO.customer_type,
                SalesKBBIO.item_details == BusyPricingKBBIO.item_name,
            ))

        query = join_query.filter(
            and_(
                SalesKBBIO.date.between(from_date, to_date),
                func.abs(cast((SalesKBBIO.main_price + SalesKBBIO.discount_amt), Numeric(10,2)) - cast(BusyPricingKBBIO.selling_price, Numeric(10,2))) > 1,
                SalesKBBIO.party_type == "Dealer", BusyPricingKBBIO.selling_price != 0,
            ))
        if exceptions:
            query = query.filter(~SalesKBBIO.voucher_no.in_(exceptions))
        results = query.with_entities(
            SalesKBBIO.date, SalesKBBIO.voucher_no, 
            SalesKBBIO.dealer_code, SalesKBBIO.particulars, 
            SalesKBBIO.item_details,           
            cast(SalesKBBIO.main_price + SalesKBBIO.discount_amt, Numeric(10,2)).label('total_price'),
            SalesKBBIO.main_price, BusyPricingKBBIO.selling_price, SalesKBBIO.discount_amt, 
            SalesKBBIO.main_qty, SalesKBBIO.main_unit, SalesKBBIO.material_centre
        ).all()

        df_results = pd.DataFrame(results, columns=[
            'Date', 'Invoice No', 'Dealer Code', 
            'Particulars', 'Sales_Item_Name', 'Total Price', 
            'Sales_Price', 'Price_List', 'Discount_Amt', 
            'Qty', 'Unit', 'Material Centre'
        ])

        return df_results


