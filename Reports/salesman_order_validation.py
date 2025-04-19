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

class VolumeDiscountValidation:

    def __init__(self, db_connector):
        self.db_connector = db_connector
        self.Session = scoped_session(sessionmaker(bind=self.db_connector.engine, autoflush=False))


    def volume_discount_validation(self, dates:list, exceptions:list = None) -> pd.DataFrame:

            def calculate_remark(row):
                slabs = [
                        ('Others', 50, 99, 2),
                        ('Others', 100, 199, 4),
                        ('Others', 200, 399, 6),
                        ('Others', 400, 750, 8),
                        ('Others', 751, float('inf'), 10),
                        ('Granules', 500, 999, 2),
                        ('Granules', 1000, 2499, 3),
                        ('Granules', 2500, 4999, 5),
                        ('Granules', 5000, float('inf'), 7),
                        ]

                if row['item_category'] == 'Others' and row['total_qty'] < 50:
                    return 'Match' if row['volume_disc'] == 0 else 'Discrepancy'

                for item_cat, lower, upper, discount in slabs:
                    if row['item_category'] == item_cat and lower <= row['total_qty'] <= upper:
                        if row['volume_disc'] < discount:
                            return 'Less Discount'
                        elif row['volume_disc'] == discount:
                            return 'Match'

                if row['item_category'] == 'Granules' and row['total_qty'] < 500:
                    return 'Match' if row['volume_disc'] == 0 else 'Discrepancy'
                
                if row['item_category'] == 'Organeem' and row['total_qty'] <= 50:
                    return 'Match' if row['volume_disc'] == 0 else 'Discrepancy'

                return 'Discrepancy'
                
            item_catergory_column = case(
                                        # (SalesKBBIO.item_details.contains('Organeem'), 'Organeem'),
                                        (SalesKBBIO.item_details.contains('Granules'), 'Granules'),
                                        (SalesKBBIO.item_details.contains('Tunner'), 'Tunner'),
                                    else_='Others').label('item_category')
            
            volume_disc = cast(case(
                                (and_(SalesKBBIO.discount_perc < 25, item_catergory_column == 'Others'), SalesKBBIO.discount_perc),
                                (and_(SalesKBBIO.discount_perc > 25, item_catergory_column == 'Others'), SalesKBBIO.discount_perc - 25),
                                (and_(SalesKBBIO.discount_perc < 20, item_catergory_column == 'Granules'), SalesKBBIO.discount_perc),
                                (and_(SalesKBBIO.discount_perc > 20, item_catergory_column == 'Granules'), SalesKBBIO.discount_perc - 20),
                            else_=0).label('volume_disc'), DECIMAL(10, 2))
            
            cash_disc = case((SalesKBBIO.discount_perc >= 25, 25), else_= 0).label('cash_disc')

            query = self.Session.query(SalesKBBIO.date, SalesKBBIO.voucher_no, SalesKBBIO.alt_qty, 
                                    SalesKBBIO.item_details, SalesKBBIO.particulars, 
                                    SalesKBBIO.discount_perc, item_catergory_column, volume_disc, cash_disc,
                                    ).filter(and_(SalesKBBIO.party_type == 'Dealer', SalesKBBIO.date.in_(dates),
                                                item_catergory_column != 'Tunner', 
                                        )).filter(~SalesKBBIO.material_centre.like('NA %'),
                                                ~SalesKBBIO.material_centre.like('GE %'), 
                                                ~SalesKBBIO.material_centre.like('AS %'),
                                                )
            if exceptions:
                query = query.filter(~SalesKBBIO.dealer_code.in_(exceptions))

            group_query = query.group_by(SalesKBBIO.date, SalesKBBIO.particulars, 
                                        item_catergory_column, SalesKBBIO.discount_perc, volume_disc, cash_disc,
                                        )
            entity_query = group_query.order_by(SalesKBBIO.date, SalesKBBIO.particulars, 
                                                
                            ).with_entities(
                                        SalesKBBIO.date, SalesKBBIO.particulars, 
                                        item_catergory_column,
                                        cast(func.sum(SalesKBBIO.alt_qty).label('total_qty'), Numeric()), 
                                        SalesKBBIO.discount_perc, volume_disc, cash_disc)
                                    
            # df = pd.read_sql(entity_query.statement, self.Session.bind)
            df = pd.DataFrame(entity_query, columns= ['date', 'particulars', 
                                                    'item_category', 
                                            'total_qty', 'disc_perc',
                                                'volume_disc', 'cash_disc', 
                                            ])
            df['remark'] = df.apply(calculate_remark, axis= 1)

            return df