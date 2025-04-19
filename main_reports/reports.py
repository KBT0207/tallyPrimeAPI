from sqlalchemy import insert, distinct, and_, or_, case, func, cast, DECIMAL, select, Numeric, Table, text, MetaData
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
import numpy as np
import datetime as dt
import os
from xlwings import view
from database.db_crud import DatabaseCrud
from logging_config import logger
# from utils.email import email_send
from database.models.busy_models.busy_pricing import BusyPricingKBBIO
from database.models.busy_models.busy_accounts import (BusyAccounts100x, BusyAccountsAgri, 
                                                    BusyAccountsGreenEra, BusyAccountsKBBIO,
                                                    BusyAccountsNewAge, )
from database.models.busy_models.busy_reports import (SalesKBBIO, SalesOrderKBBIO, SalesReturnKBBIO, MITPKBBIO, MRFPKBBIO)
from database.models.tally_models.tally_report_models import (TallyAccounts, TallyOutstandingBalance, 
                                                              TallySales, TallySalesReturn, TallyJournal, 
                                                              TallyPayment, TallyPurchase, TallyPurchaseReturn ,
                                                              TallyReceipts, DebtorsBalance
                                                              )

pd.set_option('display.max_columns', None)


class Reports(DatabaseCrud):

    def sales_price_validation(self, from_date:str, to_date:str, effective_date:str, exceptions:list = None) -> pd.DataFrame:
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
                effective_date == BusyPricingKBBIO.effective_from,
            ))

        query = join_query.filter(
            and_(
                SalesKBBIO.date.between(from_date, to_date),
                func.abs(cast((SalesKBBIO.main_price + SalesKBBIO.discount_amt), Numeric(10,2)) - cast(BusyPricingKBBIO.selling_price, Numeric(10,2))) > 1,
                SalesKBBIO.party_type == "Dealer", BusyPricingKBBIO.selling_price != 0,
            ))
        if exceptions:
            query = query.filter(~SalesKBBIO.voucher_no.in_(exceptions))
        results = query.with_entities(SalesKBBIO.date, SalesKBBIO.voucher_no, 
                                                SalesKBBIO.dealer_code, SalesKBBIO.particulars, 
                                                SalesKBBIO.item_details,           
            cast(SalesKBBIO.main_price + SalesKBBIO.discount_amt, Numeric(10,2)).label('total_price'),
            SalesKBBIO.main_price, BusyPricingKBBIO.selling_price, SalesKBBIO.discount_amt, 
            SalesKBBIO.main_qty, SalesKBBIO.main_unit , SalesKBBIO.material_centre,
                                ).all()

        df_results = pd.DataFrame(results, columns=['Date', 'Invoice No', 'Dealer Code', 
                                                    'Particulars', 'Sales_Item_Name', 'Total Price', 
                                                    'Sales_Price', 'Price_List', 'Discount_Amt', 
                                                    'Qty', 'Unit', 'Material Centre', 
                                                    ])

        return df_results

 

    def salesman_order_validation(self, from_date:str, to_date:str, exceptions:list = None) -> pd.DataFrame:
        
        salesorder = self.Session.query(SalesOrderKBBIO).filter(and_(SalesOrderKBBIO.date.between(from_date, to_date),
                                                        SalesOrderKBBIO.salesman.is_(None), SalesOrderKBBIO.salesman == None))
        if exceptions:
            salesorder = salesorder.filter(SalesOrderKBBIO.voucher_no.in_(exceptions))
        salesorder = salesorder.with_entities(SalesOrderKBBIO.date, SalesOrderKBBIO.voucher_no, 
                                    SalesOrderKBBIO.particulars, SalesOrderKBBIO.item_details, 
                                    SalesOrderKBBIO.material_centre, SalesOrderKBBIO.main_qty, 
                                    SalesOrderKBBIO.main_unit, SalesOrderKBBIO.main_price, SalesOrderKBBIO.alt_qty, 
                                    SalesOrderKBBIO.alt_unit, SalesOrderKBBIO.alt_price, SalesOrderKBBIO.amount, 
                                    SalesOrderKBBIO.tax_amt, SalesOrderKBBIO.order_amt, SalesOrderKBBIO.salesman, 
                                    SalesOrderKBBIO.salesman_id,
                                   ).all()
        df_salesorder = pd.DataFrame(salesorder, 
                                     columns=['Date', 'Voucher No', 'Particulars', 'Item Details', 
                                              'Material Centre', 'Main Qty', 'Main Unit', 'Main Price', 
                                              'Alt Qty', 'Alt Unit', 'Alt Price', 'Amount', 'Tax Amnt', 
                                              'Order Amnt', 'Salesman Name', 'Salesman ID',
                                                    ])
        return df_salesorder
    
    
    
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
            
            if row['item_category'] == 'Organeem' and row['total_qty'] >= 50:
                return 'Match' if row['volume_disc'] == 51 else 'Discrepancy'
            
            if row['item_category'] == 'Balanstick' and row['total_qty'] >= 250:
                return 'Match' if row['volume_disc'] >= 36.97 else 'Discrepancy' 

            for item_cat, lower, upper, discount in slabs:
                if row['item_category'] == item_cat and lower <= row['total_qty'] <= upper:
                    if row['volume_disc'] <= discount:
                        return 'Less Discount'
                    elif row['volume_disc'] == discount:
                        return 'Match'

            if row['item_category'] == 'Granules' and row['total_qty'] < 500:
                return 'Match' if row['volume_disc'] == 0 else 'Discrepancy'
            
            if row['item_category'] == 'Organeem' and row['total_qty'] <= 50:
                    return 'Match' if row['volume_disc'] == 0 else 'Discrepancy'
            
                        

            return 'Discrepancy'
            
        item_catergory_column = case(
                                (and_(SalesKBBIO.item_details.contains('Organeem'), SalesKBBIO.discount_perc == 51), 'Organeem'),
                                (and_(SalesKBBIO.item_details.contains('Balanstick'), SalesKBBIO.discount_perc >= 36.97), 'Balanstick'),
                                (SalesKBBIO.item_details.contains('Granules'), 'Granules'),
                                (SalesKBBIO.item_details.contains('Tunner'), 'Tunner'),
                            else_='Others').label('item_category')
        
        volume_disc = cast(case(
                            (and_(SalesKBBIO.discount_perc >= 36.90, item_catergory_column == 'Balanstick'), SalesKBBIO.discount_perc),
                            (and_(SalesKBBIO.discount_perc < 37, item_catergory_column == 'Balanstick'), SalesKBBIO.discount_perc),
                            (and_(SalesKBBIO.discount_perc < 25, item_catergory_column == 'Others'), SalesKBBIO.discount_perc),
                            (and_(SalesKBBIO.discount_perc > 25, item_catergory_column == 'Others'), SalesKBBIO.discount_perc - 25),
                            (and_(SalesKBBIO.discount_perc < 20, item_catergory_column == 'Granules'), SalesKBBIO.discount_perc),
                            (and_(SalesKBBIO.discount_perc > 20, item_catergory_column == 'Granules'), SalesKBBIO.discount_perc - 20),
                            (and_(SalesKBBIO.discount_perc == 51, item_catergory_column == 'Organeem'), SalesKBBIO.discount_perc),
                        else_=0).label('volume_disc'), DECIMAL(10, 2))
        
        cash_disc = case(
                    (and_(SalesKBBIO.item_details.contains('Granules'), SalesKBBIO.discount_perc >= 20), 20),
                    (and_(~SalesKBBIO.item_details.contains('Granules'), SalesKBBIO.discount_perc >= 25), 25),
                        else_=0
                    ).label('cash_disc')
        
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
                                
        df = pd.DataFrame(entity_query, columns= ['date', 'particulars', 
                                                  'item_category', 
                                           'total_qty', 'disc_perc',
                                             'volume_disc', 'cash_disc', 
                                           ])
        df['remark'] = df.apply(calculate_remark, axis= 1)

        return df


    # make it efficient
    def cash_discount_validation(self, dates:list, exceptions:list = None) -> pd.DataFrame:
        #main busy sales query
        sales_query = self.Session.query(SalesKBBIO.date, SalesKBBIO.voucher_no,  SalesKBBIO.alt_qty, 
                                   SalesKBBIO.item_details, SalesKBBIO.particulars, 
                                   SalesKBBIO.discount_perc, SalesKBBIO.dealer_code,
                                ).filter(and_(SalesKBBIO.party_type == 'Dealer', SalesKBBIO.date.in_(dates),
                                            SalesKBBIO.discount_perc >= 20),
                                            ~SalesKBBIO.material_centre.like('NA %'),
                                            ~SalesKBBIO.material_centre.like('GE %'), 
                                            ~SalesKBBIO.material_centre.like('AS %'),
                                            )
 
        sales_distinct_invoice_query = sales_query.distinct(SalesKBBIO.voucher_no)
        
        sales_distinct_dealer_query = sales_query.distinct(SalesKBBIO.dealer_code)

        if exceptions:
            sales_distinct_invoice_query = sales_distinct_invoice_query.filter(~SalesKBBIO.dealer_code.in_(exceptions))
            sales_distinct_dealer_query = sales_distinct_dealer_query.filter(~SalesKBBIO.dealer_code.in_(exceptions))
        
        #busy sales distinct invoice query
        sales_distinct_invoice_query = sales_distinct_invoice_query.with_entities(SalesKBBIO.date, SalesKBBIO.voucher_no, 
                                            SalesKBBIO.particulars, SalesKBBIO.dealer_code, 
                                            SalesKBBIO.discount_perc,
                                    ).order_by(SalesKBBIO.date, SalesKBBIO.dealer_code)
        #busy sales distinct dealer query
        sales_distinct_dealer_query = sales_distinct_dealer_query.with_entities(SalesKBBIO.date, 
                                            SalesKBBIO.particulars, SalesKBBIO.dealer_code, 
                                    )
        tally_accounts_query = (sales_distinct_dealer_query.outerjoin(TallyAccounts, 
                                                                      SalesKBBIO.dealer_code == TallyAccounts.alias_code
                                                                      ).with_entities(
                                        SalesKBBIO.date.label('sales_date'), 
                                        SalesKBBIO.dealer_code.label('sales_dealer_code'), 
                                        TallyAccounts.alias_code.label('tally_alias_code'), 
                                        SalesKBBIO.particulars.label('sales_particulars'), 
                                        TallyAccounts.ledger_name.label('tally_particulars'),
                                            )
                                            ).subquery()

        tally_code_query = sales_distinct_dealer_query.outerjoin(TallyAccounts, 
                                                                      SalesKBBIO.dealer_code == TallyAccounts.alias_code
                                                                      ).with_entities(
                                        TallyAccounts.alias_code.label('tally_alias_code'), 
                                        TallyAccounts.ledger_name.label('tally_particulars'),
                                            )

        outstanding_query = (self.Session.query(
                                    TallyOutstandingBalance.particulars, 
                                    tally_accounts_query.c.tally_alias_code, tally_accounts_query.c.sales_dealer_code, 

                                    (func.sum(TallyOutstandingBalance.credit) - func.sum(TallyOutstandingBalance.debit)).label("Cr Balance")
                                )
                                .outerjoin(tally_accounts_query,
                                    (TallyOutstandingBalance.particulars == tally_accounts_query.c.tally_particulars) &
                                    (TallyOutstandingBalance.date == tally_accounts_query.c.sales_date)
                                )
                                .filter(tally_accounts_query.c.tally_particulars != None)
                                .group_by(TallyOutstandingBalance.date, 
                                    TallyOutstandingBalance.particulars,  
                                    tally_accounts_query.c.tally_alias_code, 
                                    tally_accounts_query.c.sales_dealer_code, 
                                )
                            )
                      
        sales_invoice_df = pd.DataFrame(sales_distinct_invoice_query, columns= ['busy_date', 'invoice_no', 'busy_particulars', 
                                                  'busy_dealer_code', 'disc_perc', 
                                           ])
        
        tally_code_df = pd.DataFrame(tally_code_query, 
                                         columns= ['tally_dealer_code_new', 
                                                   'tally_particulars_new',
                                                   ])
        # outstanding_df = pd.DataFrame(outstanding_query, 
        #                               columns=['outstanding_date', 'outstanding_particulars', 
        #                                        'outs_debit', 'outs_credit', 'material_centre',
        #                                        'sales_date', 'sales_dealer_code', 'tally_alias_code', 
        #                                        'sales_particulars', 'tally_particulars', 
        #                                        ]
        #                                 )
        outstanding_df = pd.DataFrame(outstanding_query, 
                                      columns=['outstanding_particulars', 
                                               'tally_alias_code', 'sales_dealer_code', 'Cr Balance', 
                                               ])
        
        results_df = sales_invoice_df.merge(outstanding_df, how= 'left', 
                                            left_on= 'busy_dealer_code', right_on= 'tally_alias_code').fillna(0)
                
        results_df['remark'] = np.where(results_df['Cr Balance'] >= 0, 'Matched', 'Discrepancy')
        results_df = results_df.sort_values(by=['busy_date', 'busy_particulars'])
        results_df['Cr Balance'] = pd.to_numeric(results_df['Cr Balance'])
        results_df = results_df.merge(tally_code_df, how= 'left', 
                                      left_on= 'busy_dealer_code', right_on= 'tally_dealer_code_new')
       
        from xlwings import view
        # return sales_invoice_df, view(outstanding_df)
        return results_df
        # return tally_df

        

    def sales_validation(self, fromdate:str, todate:str, exceptions:list) -> str:
        
        def busy_to_tally():
            busy_query = self.Session.query(SalesKBBIO.date, SalesKBBIO.voucher_no, 
                                            SalesKBBIO.party_type, SalesKBBIO.dealer_code, 
                                            SalesKBBIO.particulars, SalesKBBIO.material_centre,
                                            SalesKBBIO.amount, SalesKBBIO.tax_amt, 
                                            SalesKBBIO.gst_no,
                                    ).filter(SalesKBBIO.date.between(fromdate, todate),
                                            ~SalesKBBIO.material_centre.like('GE %'),
                                            ~SalesKBBIO.material_centre.like('NA %'),
                                            ~SalesKBBIO.material_centre.like('AS %'), 
                                            SalesKBBIO.material_centre != 'Pune', 
                                                            )
        
            tally_query = self.Session.query(TallySales.date, TallySales.voucher_no, 
                                         TallySales.particulars, cast(TallySales.debit,DECIMAL(10,2)), 
                                         TallySales.material_centre,
                                    ).outerjoin(TallyAccounts, TallySales.particulars == TallyAccounts.ledger_name
                                ).filter(~TallySales.material_centre.like('GE %'),
                                        ~TallySales.material_centre.like('NA %'),
                                        ~TallySales.material_centre.like('AS %'),
                                        TallySales.material_centre != 'Pune', 
                                            ).with_entities(TallySales.date, TallySales.voucher_no, 
                                         TallySales.particulars, cast(TallySales.debit,DECIMAL(10,2)), 
                                         TallySales.material_centre, TallyAccounts.gst_no,
                                            )
            if exceptions:
                busy_query = busy_query.filter(~SalesKBBIO.voucher_no.in_(exceptions))
                tally_query = tally_query.filter(~TallySales.voucher_no.in_(exceptions))

            group_busy_query = busy_query.with_entities(SalesKBBIO.date, 
                                            SalesKBBIO.voucher_no, SalesKBBIO.party_type, 
                                            SalesKBBIO.dealer_code, SalesKBBIO.particulars, 
                                            SalesKBBIO.gst_no, SalesKBBIO.material_centre,  
                                            cast(func.sum(SalesKBBIO.amount), DECIMAL(10, 2)).label("amt"),
                                            cast(func.sum(SalesKBBIO.tax_amt), DECIMAL(10, 2)).label("tax_amt"),
                                            cast(func.sum(SalesKBBIO.amount + SalesKBBIO.tax_amt), DECIMAL(10, 2)).label("bill_amt"),
                                        ).group_by(SalesKBBIO.date, SalesKBBIO.voucher_no,
                                            SalesKBBIO.party_type, SalesKBBIO.dealer_code,
                                            SalesKBBIO.particulars, SalesKBBIO.gst_no, 
                                            SalesKBBIO.material_centre,
                                        )
            
            busy_df = pd.DataFrame(group_busy_query, columns=['busy_invoice_date', 'busy_invoice_no', 'party_type', 
                                                              'dealer_code', 'busy_particulars', 'busy_gst_no', 
                                                              'busy_material_centre', 'amt', 'tax_amt', 'bill_amt'])
            columns = ['amt', 'tax_amt', 'bill_amt']
            for col in columns:
                busy_df[col] = pd.to_numeric(busy_df[col])

            tally_df = pd.DataFrame(tally_query, columns=['tally_invoice_date', 'tally invoice_no', 'tally_particulars', 
                                                       'debit', 'tally_material_centre', 'tally_gst_no'])
            tally_df['debit'] = pd.to_numeric(tally_df['debit'])
            
            def remove_trailing_zeros(row:str):
                if '/' in row:
                    parts = row.split('/')
                    parts[-1] = str(int(parts[-1]))
                    return '/'.join(parts)
                else:
                    return row
                
            def gst_validation(row):
                if row['busy_gst_no']:
                    if row['busy_gst_no'] == row['tally_gst_no']:
                        return "Matched"
                    else:
                        return "Not Matched"
                else:
                    return "Not Required"
                
            tally_df['updated_tally_invoice_no'] = tally_df['tally invoice_no'].apply(remove_trailing_zeros)
            tally_df = tally_df.drop_duplicates(subset='updated_tally_invoice_no')
            busy_to_tally_df = busy_df.merge(tally_df, how='left', 
                                            left_on= 'busy_invoice_no', right_on= 'updated_tally_invoice_no')
            busy_to_tally_df['amount_diff'] = pd.to_numeric(busy_to_tally_df['bill_amt'] - busy_to_tally_df['debit']).abs()
            busy_to_tally_df['gst_remark'] = busy_to_tally_df.apply(gst_validation, axis=1)

            return busy_to_tally_df

        
        def tally_to_busy():
            tally_query = self.Session.query(TallySales.date, TallySales.voucher_no, 
                                         TallySales.particulars, cast(TallySales.debit,DECIMAL(10,2)), 
                                         TallySales.material_centre, 
                                    ).outerjoin(TallyAccounts, TallySales.particulars == TallyAccounts.ledger_name
                                ).filter(TallySales.date.between(fromdate, todate), 
                                        ~TallySales.material_centre.like('GE %'),
                                        ~TallySales.material_centre.like('NA %'),
                                        ~TallySales.material_centre.like('AS %'),
                                        TallySales.material_centre != 'Pune', 
                                            ).with_entities(TallySales.date, TallySales.voucher_no, 
                                         TallySales.particulars, cast(TallySales.debit,DECIMAL(10,2)), 
                                         TallySales.material_centre, TallyAccounts.ledger_name, 
                                            )
        
            busy_query = self.Session.query(SalesKBBIO.date, SalesKBBIO.voucher_no, 
                                         SalesKBBIO.party_type, SalesKBBIO.dealer_code, 
                                         SalesKBBIO.particulars, SalesKBBIO.amount, 
                                         SalesKBBIO.tax_amt, SalesKBBIO.gst_no,
                                ).filter(~SalesKBBIO.material_centre.like('GE %'),
                                        ~SalesKBBIO.material_centre.like('NA %'),
                                        ~SalesKBBIO.material_centre.like('AS %'), 
                                        SalesKBBIO.material_centre != 'Pune', 
                                                        )
            
            if exceptions:
                tally_query = tally_query.filter(~TallySales.voucher_no.in_(exceptions))
                busy_query = busy_query.filter(~SalesKBBIO.voucher_no.in_(exceptions))

            group_busy_query = busy_query.with_entities(SalesKBBIO.date, 
                                            SalesKBBIO.voucher_no, SalesKBBIO.party_type, 
                                            SalesKBBIO.dealer_code, SalesKBBIO.particulars, SalesKBBIO.gst_no,
                                            cast(func.sum(SalesKBBIO.amount), DECIMAL(10, 2)).label("amt"),
                                            cast(func.sum(SalesKBBIO.tax_amt), DECIMAL(10, 2)).label("tax_amt"),
                                            cast(func.sum(SalesKBBIO.amount + SalesKBBIO.tax_amt), DECIMAL(10, 2)).label("bill_amt"),
                                        ).group_by(
                                            SalesKBBIO.date, SalesKBBIO.voucher_no,
                                            SalesKBBIO.party_type, SalesKBBIO.dealer_code,
                                            SalesKBBIO.particulars, SalesKBBIO.gst_no, 
                                        )
            
            busy_df = pd.DataFrame(group_busy_query, columns=['busy_invoice_date', 'busy_invoice_no', 'party_type', 'dealer_code', 
                                        'busy_particulars', 'busy_gst_no', 'amt', 'tax_amt', 'bill_amt'])
            columns = ['amt', 'tax_amt', 'bill_amt']
            for col in columns:
                busy_df[col] = pd.to_numeric(busy_df[col])

            tally_df = pd.DataFrame(tally_query, columns=['tally_invoice_date', 'tally invoice_no', 'tally_particulars', 
                                                       'debit', 'material_centre', 'tally_gst_no'])
            tally_df['debit'] = pd.to_numeric(tally_df['debit'])
        
            def remove_trailing_zeros(row:str):
                if '/' in row:
                    parts = row.split('/')
                    parts[-1] = str(int(parts[-1]))
                    return '/'.join(parts)
                else:
                    return row
                
            def gst_validation(row):
                if row['tally_gst_no']:
                    if row['tally_gst_no'] == row['busy_gst_no']:
                        return "Matched"
                    else:
                        return "Not Matched"
                else:
                    return "Not Required"
                
            tally_df['updated_tally_invoice_no'] = tally_df['tally invoice_no'].apply(remove_trailing_zeros)
            tally_df = tally_df.drop_duplicates(subset='updated_tally_invoice_no')
            tally_to_busy_df = tally_df.merge(busy_df, how='left', 
                                            left_on= 'updated_tally_invoice_no', right_on= 'busy_invoice_no')
            tally_to_busy_df['amount_diff'] = pd.to_numeric(tally_to_busy_df['bill_amt'] - tally_to_busy_df['debit']).abs()
            tally_to_busy_df['gst_remark'] = tally_to_busy_df.apply(gst_validation, axis=1)
            # from xlwings import view
            # return view(tally_to_busy_df)
            return tally_to_busy_df

        result_busy_to_tally = busy_to_tally()
        result_tally_to_busy = tally_to_busy()

        file_path = fr'D:\Reports\Sales_Reco\Busy-Tally Sales Reco ({fromdate} to {todate}).xlsx'

        with pd.ExcelWriter(file_path) as writer:
            result_busy_to_tally.to_excel(writer, sheet_name='Busy Sales', index=False)
            result_tally_to_busy.to_excel(writer, sheet_name='Tally Sales', index=False)

        return file_path



    def sales_return_validation(self, fromdate:str, todate:str, exceptions:list) -> str:
        
        def busy_to_tally():
            busy_query = self.Session.query(SalesReturnKBBIO.date, SalesReturnKBBIO.voucher_no, 
                                            SalesReturnKBBIO.party_type, SalesReturnKBBIO.dealer_code, 
                                            SalesReturnKBBIO.particulars, SalesReturnKBBIO.material_centre,
                                            SalesReturnKBBIO.amount, SalesReturnKBBIO.tax_amt, 
                                            SalesReturnKBBIO.gst_no, 
                                    ).filter(SalesReturnKBBIO.date.between(fromdate, todate),
                                            ~SalesReturnKBBIO.material_centre.like('GE %'),
                                            ~SalesReturnKBBIO.material_centre.like('NA %'),
                                            ~SalesReturnKBBIO.material_centre.like('AS %'), 
                                            SalesReturnKBBIO.material_centre != 'Pune', 
                                                            )
        
            tally_query = self.Session.query(TallySalesReturn.date, TallySalesReturn.voucher_no, 
                                         TallySalesReturn.particulars, cast(TallySalesReturn.credit,DECIMAL(10,2)), 
                                         TallySalesReturn.material_centre, 
                                    ).outerjoin(TallyAccounts, TallySalesReturn.particulars == TallyAccounts.ledger_name
                                ).filter(~TallySalesReturn.material_centre.like('GE %'),
                                        ~TallySalesReturn.material_centre.like('NA %'),
                                        ~TallySalesReturn.material_centre.like('AS %'),
                                        TallySalesReturn.material_centre != 'Pune', 
                                            ).with_entities(TallySalesReturn.date, TallySalesReturn.voucher_no, 
                                        TallySalesReturn.particulars, cast(TallySalesReturn.credit,DECIMAL(10,2)), 
                                        TallySalesReturn.material_centre, TallyAccounts.gst_no, 
                                                        )
            if exceptions:
                busy_query = busy_query.filter(~SalesReturnKBBIO.voucher_no.in_(exceptions))
                tally_query = tally_query.filter(~TallySalesReturn.voucher_no.in_(exceptions))

            group_busy_query = busy_query.with_entities(SalesReturnKBBIO.date, 
                                            SalesReturnKBBIO.voucher_no, SalesReturnKBBIO.party_type, 
                                            SalesReturnKBBIO.dealer_code, SalesReturnKBBIO.particulars, 
                                            SalesReturnKBBIO.gst_no, SalesReturnKBBIO.material_centre, 
                                            cast(func.sum(SalesReturnKBBIO.amount), DECIMAL(10, 2)).label("amt"),
                                            cast(func.sum(SalesReturnKBBIO.tax_amt), DECIMAL(10, 2)).label("tax_amt"),
                                            cast(func.sum(SalesReturnKBBIO.amount + SalesReturnKBBIO.tax_amt), DECIMAL(10, 2)).label("bill_amt"),
                                        ).group_by(
                                            SalesReturnKBBIO.date, SalesReturnKBBIO.voucher_no,
                                            SalesReturnKBBIO.party_type, SalesReturnKBBIO.dealer_code,
                                            SalesReturnKBBIO.particulars, SalesReturnKBBIO.material_centre, 
                                            SalesReturnKBBIO.gst_no,
                                        )
            
            busy_df = pd.DataFrame(group_busy_query, columns=['busy_invoice_date', 'busy_invoice_no', 'party_type', 'dealer_code', 
                                        'busy_particulars', 'busy_gst_no', 'busy_material_centre', 'amt', 'tax_amt', 'bill_amt'])
            columns = ['amt', 'tax_amt', 'bill_amt']
            for col in columns:
                busy_df[col] = pd.to_numeric(busy_df[col])

            tally_df = pd.DataFrame(tally_query, columns=['tally_invoice_date', 'tally invoice_no', 
                                                          'tally_particulars', 'credit', 'tally_material_centre', 
                                                          'tally_gst_no'])
            tally_df['credit'] = pd.to_numeric(tally_df['credit'])
            
            def remove_trailing_zeros(row: str):
                import re
                if '/' in row:
                    parts = row.split('/')
                    # Remove non-digit characters from the last part
                    cleaned_last_part = re.sub(r'\D', '', parts[-1])
                    # Convert to integer to remove leading zeros and back to string
                    if cleaned_last_part:  # Check if cleaned_last_part is not empty
                        parts[-1] = str(int(cleaned_last_part))
                    else:
                        parts[-1] = '0'  # Handle case where cleaned_last_part becomes empty
                    return '/'.join(parts)
                else:
                    cleaned_invoice_no = re.sub(r'([A-Z]+)0+([1-9][0-9]*)', r'\1\2', row)
                    return cleaned_invoice_no
                
            def gst_validation(row):
                if row['busy_gst_no']:
                    if row['busy_gst_no'] == row['tally_gst_no']:
                        return "Matched"
                    else:
                        return "Not Matched"
                else:
                    return "Not Required"
                
            busy_df['updated_busy_invoice_no'] = busy_df['busy_invoice_no'].apply(remove_trailing_zeros)    
            tally_df['updated_tally_invoice_no'] = tally_df['tally invoice_no'].apply(remove_trailing_zeros)
         
            tally_df = tally_df.drop_duplicates(subset='updated_tally_invoice_no')
            busy_to_tally_df = busy_df.merge(tally_df, how='left', 
                                            left_on= 'updated_busy_invoice_no', right_on= 'updated_tally_invoice_no')
            busy_to_tally_df['amount_diff'] = pd.to_numeric(busy_to_tally_df['bill_amt'] - busy_to_tally_df['credit']).abs()
            busy_to_tally_df['gst_remark'] = busy_to_tally_df.apply(gst_validation, axis=1)

            return busy_to_tally_df
        

        
        def tally_to_busy():
            tally_query = self.Session.query(TallySalesReturn.date, TallySalesReturn.voucher_no, 
                                         TallySalesReturn.particulars, cast(TallySalesReturn.credit,DECIMAL(10,2)), 
                                         TallySalesReturn.material_centre, TallySalesReturn.voucher_type,
                                    ).outerjoin(TallyAccounts, TallySalesReturn.particulars == TallyAccounts.ledger_name
                                ).filter(TallySalesReturn.date.between(fromdate, todate), 
                                        ~TallySalesReturn.material_centre.like('GE %'),
                                        ~TallySalesReturn.material_centre.like('NA %'),
                                        ~TallySalesReturn.material_centre.like('AS %'),
                                        TallySalesReturn.material_centre != 'Pune', 
                                        ~TallySalesReturn.voucher_type.contains('Discount'), 
                                            ).with_entities(TallySalesReturn.date, 
                                                    TallySalesReturn.voucher_no, 
                                                    TallySalesReturn.particulars, 
                                                    cast(TallySalesReturn.credit,DECIMAL(10,2)), 
                                                    TallySalesReturn.material_centre, TallyAccounts.gst_no, 
                                                    )
        
            busy_query = self.Session.query(SalesReturnKBBIO.date, SalesReturnKBBIO.voucher_no, 
                                         SalesReturnKBBIO.party_type, SalesReturnKBBIO.dealer_code, 
                                         SalesReturnKBBIO.particulars, SalesReturnKBBIO.amount, 
                                         SalesReturnKBBIO.tax_amt, SalesReturnKBBIO.gst_no, 
                                ).filter(~SalesReturnKBBIO.material_centre.like('GE %'),
                                        ~SalesReturnKBBIO.material_centre.like('NA %'),
                                        ~SalesReturnKBBIO.material_centre.like('AS %'), 
                                        SalesReturnKBBIO.material_centre != 'Pune', 
                                                        )
            
            if exceptions:
                tally_query = tally_query.filter(~TallySalesReturn.voucher_no.in_(exceptions))
                busy_query = busy_query.filter(~SalesReturnKBBIO.voucher_no.in_(exceptions))

            group_busy_query = busy_query.with_entities(SalesReturnKBBIO.date, 
                                            SalesReturnKBBIO.voucher_no, SalesReturnKBBIO.party_type, 
                                            SalesReturnKBBIO.dealer_code, SalesReturnKBBIO.particulars, 
                                            SalesReturnKBBIO.material_centre, SalesReturnKBBIO.gst_no,
                                            cast(func.sum(SalesReturnKBBIO.amount), DECIMAL(10, 2)).label("amt"),
                                            cast(func.sum(SalesReturnKBBIO.tax_amt), DECIMAL(10, 2)).label("tax_amt"),
                                            cast(func.sum(SalesReturnKBBIO.amount + SalesReturnKBBIO.tax_amt), DECIMAL(10, 2)).label("bill_amt"),
                                        ).group_by(
                                            SalesReturnKBBIO.date, SalesReturnKBBIO.voucher_no,
                                            SalesReturnKBBIO.party_type, SalesReturnKBBIO.dealer_code,
                                            SalesReturnKBBIO.particulars, SalesReturnKBBIO.material_centre, 
                                            SalesReturnKBBIO.gst_no,
                                                )
            
            busy_df = pd.DataFrame(group_busy_query, columns=['busy_invoice_date', 'busy_invoice_no', 'party_type', 
                                                              'dealer_code', 'busy_particulars', 'busy_material_centre', 
                                                              'busy_gst_no', 'amt', 'tax_amt', 'bill_amt'])
            columns = ['amt', 'tax_amt', 'bill_amt']
            for col in columns:
                busy_df[col] = pd.to_numeric(busy_df[col])

            tally_df = pd.DataFrame(tally_query, columns=['tally_invoice_date', 'tally_invoice_no', 'tally_particulars', 
                                                       'credit', 'tally_material_centre', 'tally_gst_no'])
            tally_df['credit'] = pd.to_numeric(tally_df['credit'])
        
            def remove_trailing_zeros(row: str):
                import re
                if '/' in row:
                    parts = row.split('/')
                    # Remove non-digit characters from the last part
                    cleaned_last_part = re.sub(r'\D', '', parts[-1])
                    # Convert to integer to remove leading zeros and back to string
                    if cleaned_last_part:  # Check if cleaned_last_part is not empty
                        parts[-1] = str(int(cleaned_last_part))
                    else:
                        parts[-1] = '0'  # Handle case where cleaned_last_part becomes empty
                    return '/'.join(parts)
                else:
                    cleaned_invoice_no = re.sub(r'([A-Z]+)0+([1-9][0-9]*)', r'\1\2', row)
                    return cleaned_invoice_no
                
            def gst_validation(row):
                if row['busy_gst_no']:
                    if row['busy_gst_no'] == row['tally_gst_no']:
                        return "Matched"
                    else:
                        return "Not Matched"
                else:
                    return "Not Required"

            tally_df['updated_tally_invoice_no'] = tally_df['tally_invoice_no'].apply(remove_trailing_zeros)
            busy_df['updated_busy_invoice_no'] = busy_df['busy_invoice_no'].apply(remove_trailing_zeros)
            tally_df = tally_df.drop_duplicates(subset='updated_tally_invoice_no')
            tally_to_busy_df = tally_df.merge(busy_df, how='left', 
                                            left_on= 'updated_tally_invoice_no', right_on= 'updated_busy_invoice_no')
            tally_to_busy_df['amount_diff'] = pd.to_numeric(tally_to_busy_df['bill_amt'] - tally_to_busy_df['credit']).abs()
            tally_to_busy_df['gst_remark'] = tally_to_busy_df.apply(gst_validation, axis=1)

            from xlwings import view
            # return view(tally_to_busy_df)
            return tally_to_busy_df

        result_busy_to_tally = busy_to_tally()
        result_tally_to_busy = tally_to_busy()
      
        file_path = fr'D:\Reports\Sales_Return_Reco\Busy-Tally Sales Return Reco ({fromdate} to {todate}).xlsx'

        with pd.ExcelWriter(file_path) as writer:
            result_busy_to_tally.to_excel(writer, sheet_name='Busy Sales Return', index=False)
            result_tally_to_busy.to_excel(writer, sheet_name='Tally Sales Return', index=False)
        
        return file_path



    def salesorder_mitp_reco(self, fromdate:str, todate:str, exceptions:list) -> pd.DataFrame:

        salesorder_query = self.Session.query(SalesOrderKBBIO.date, SalesOrderKBBIO.voucher_no, 
                                             SalesOrderKBBIO.particulars, SalesOrderKBBIO.item_details, 
                                             SalesOrderKBBIO.material_centre, SalesOrderKBBIO.main_qty, 
                                             SalesOrderKBBIO.main_unit,
                                             func.sum(SalesOrderKBBIO.main_qty).label('salesorder_qty'), 
                            ).filter(SalesOrderKBBIO.date.between(fromdate, todate), 
                                ).group_by(SalesOrderKBBIO.date, SalesOrderKBBIO.voucher_no, 
                                             SalesOrderKBBIO.particulars, SalesOrderKBBIO.item_details, 
                                             SalesOrderKBBIO.material_centre, SalesOrderKBBIO.main_unit, 
                                ).order_by(SalesOrderKBBIO.date, SalesOrderKBBIO.voucher_no
                                            ).with_entities(SalesOrderKBBIO.date, SalesOrderKBBIO.voucher_no, 
                                                            SalesOrderKBBIO.particulars, SalesOrderKBBIO.item_details, 
                                                            SalesOrderKBBIO.material_centre, 
                                                            func.sum(SalesOrderKBBIO.main_qty).label('salesorder_qty'), 
                                                            SalesOrderKBBIO.main_unit, 
                                                            )
        mitp_query = self.Session.query(MITPKBBIO.date, MITPKBBIO.voucher_no, MITPKBBIO.particulars, 
                                        MITPKBBIO.item_details, MITPKBBIO.material_centre, 
                                        MITPKBBIO.sales_order_no, MITPKBBIO.main_qty, MITPKBBIO.main_unit, 
                                        func.sum(MITPKBBIO.main_qty).label('mitp_total_qty'), 
                                        ).group_by(MITPKBBIO.particulars, MITPKBBIO.item_details, 
                                                   MITPKBBIO.material_centre, MITPKBBIO.sales_order_no, 
                                                   MITPKBBIO.main_unit, 
                                            ).with_entities(MITPKBBIO.sales_order_no, MITPKBBIO.particulars, 
                                                            MITPKBBIO.item_details, MITPKBBIO.material_centre, 
                                                            func.sum(MITPKBBIO.main_qty).label('mitp_total_qty'), 
                                                            MITPKBBIO.main_unit, 
                                                            ) 
        if exceptions:
            salesorder_query = salesorder_query.filter(SalesOrderKBBIO.voucher_no.in_(exceptions))

        salesorder_df = pd.DataFrame(salesorder_query, columns= ['salesorder_date', 'salesorder_no', 'salesorder_particulars', 
                                                                 'salesorder_items', 'salesorder_material_centre', 
                                                                 'salesorder_qty', 'salesorder_unit',
                                                                 ])
        mitp_df = pd.DataFrame(mitp_query, columns= ['mitp_salesorder_no', 'mitp_particulars', 
                                                     'mitp_items', 'mitp_material_centre', 
                                                     'mitp_total_qty', 'mitp_unit', 
                                                     ])
        result_df = salesorder_df.merge(mitp_df, how='left', 
                                        left_on= ['salesorder_no', 'salesorder_items', 'salesorder_material_centre', 'salesorder_unit', ], 
                                        right_on= ['mitp_salesorder_no', 'mitp_items', 'mitp_material_centre', 'mitp_unit', ])

        result_df['remark'] = np.where(result_df['mitp_total_qty'] > result_df['salesorder_qty'], "Discrepancy", "Pass")

        return result_df
    


    def populate_debtor_balances(self, fromdate: str, todate: str, filename: str, to_import: bool = True, to_export: bool = False, 
                             commit: bool = True, export_location: str = r'D:\Reports\Debtors_Balance') -> None:
        """
        Populate debtor balances for a given date range.

        This method fetches sales from busy and rest from tally, processes the data to calculate debtor balances, and 
        optionally imports the data into the database and/or exports it to an Excel file.

        Args:
            fromdate (str): The start date for the data in 'YYYY-MM-DD' format.
            todate (str): The end date for the data in 'YYYY-MM-DD' format.
            to_import (bool, optional): If True, import the processed data into the database.
            filename (str): The name of the Excel file to export the data to.
            to_export (bool, optional): If True, export the processed data to an Excel file. Defaults to False.
            commit (bool, optional): If True, commit the transaction when importing data into the database. Defaults to True.
            export_location (str, optional): The directory path where the Excel file will be saved. Defaults to 'D:/Reports'.

        Returns:
            None
        """
    
        # Convert string dates to datetime.date objects
        fromdate_dt = dt.datetime.strptime(fromdate, '%Y-%m-%d').date()
        todate_dt = dt.datetime.strptime(todate, '%Y-%m-%d').date()
        previous_dt = (fromdate_dt - dt.timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Check if the 'from' date is later than the 'to' date
        if todate_dt < fromdate_dt:
            return logger.critical(f"fromdate: {fromdate} should not be larger than todate: {todate}")
        
        # Query to fetch busy accounts data
        busy_acc_query = (self.Session.query(BusyAccountsKBBIO.name, BusyAccountsKBBIO.alias)
                        .filter(BusyAccountsKBBIO.alias.isnot(None), 
                                BusyAccountsKBBIO.parent_group == 'Dealer'))

        # Query to fetch busy sales data
        busy_sales_query = (self.Session.query(SalesKBBIO.dealer_code, 
                                       cast(func.sum(SalesKBBIO.amount + SalesKBBIO.tax_amt), 
                                            DECIMAL(10, 2)).label('busy_sales_amt'))
                            .filter(SalesKBBIO.party_type == 'Dealer', 
                                    SalesKBBIO.dealer_code.isnot(None), 
                                    SalesKBBIO.date.between(fromdate, todate))
                            .group_by(SalesKBBIO.dealer_code)
                            .order_by(SalesKBBIO.dealer_code))

        # Query to fetch tally outstanding balances
        tally_outstanding_query = (self.Session.query(TallyAccounts.alias_code, 
                                            func.sum(TallyOutstandingBalance.debit).label('total_debit'), 
                                            func.sum(TallyOutstandingBalance.credit).label('total_credit'), 
                                            cast(func.sum(TallyOutstandingBalance.debit - TallyOutstandingBalance.credit), 
                                                    DECIMAL(10, 2)).label("outstanding_balance"))
                                .outerjoin(TallyAccounts, 
                                           TallyOutstandingBalance.particulars == TallyAccounts.ledger_name)
                                .filter(TallyOutstandingBalance.date == previous_dt)
                                .group_by(TallyAccounts.alias_code)
                                .with_entities(TallyAccounts.alias_code, 
                                            cast(func.sum(TallyOutstandingBalance.debit - TallyOutstandingBalance.credit), 
                                                DECIMAL(10, 2)).label("outstanding_balance")))

        # Create a CTE for distinct ledger names
        distinct_ledger_names_cte = (self.Session.query(func.distinct(TallyAccounts.ledger_name).label('ledger'), 
                                                        TallyAccounts.alias_code)
                                    .cte('distinct_ledger_names'))

        # Query to fetch tally sales return data
        tally_salesreturn_query = (self.Session.query(distinct_ledger_names_cte.c.alias_code, 
                                                      cast(func.sum(TallySalesReturn.credit), 
                                                           DECIMAL(10, 2)).label("tally_salesreturn_amt"))
                                .outerjoin(distinct_ledger_names_cte, 
                                           TallySalesReturn.particulars == distinct_ledger_names_cte.c.ledger)
                                .filter(TallySalesReturn.date.between(fromdate_dt, todate_dt), 
                                        distinct_ledger_names_cte.c.alias_code != 'None')
                                .group_by(distinct_ledger_names_cte.c.alias_code)
                                .order_by(distinct_ledger_names_cte.c.alias_code)
                                .with_entities(distinct_ledger_names_cte.c.alias_code, 
                                               cast(func.sum(TallySalesReturn.credit), 
                                                    DECIMAL(10, 2)).label("tally_salesreturn_amt")))

        # Query to fetch tally purchase data
        tally_purchase_query = (self.Session.query(TallyPurchase.date, TallyPurchase.particulars, 
                                                   cast(func.sum(TallyPurchase.credit), 
                                                        DECIMAL(10, 2)).label("tally_purchase_amt"), 
                                                        distinct_ledger_names_cte.c.alias_code)
                                .outerjoin(distinct_ledger_names_cte, 
                                           TallyPurchase.particulars == distinct_ledger_names_cte.c.ledger)
                                .filter(TallyPurchase.date.between(fromdate_dt, todate_dt), 
                                        distinct_ledger_names_cte.c.alias_code != 'None')
                                .group_by(distinct_ledger_names_cte.c.alias_code)
                                .order_by(distinct_ledger_names_cte.c.alias_code)
                                .with_entities(distinct_ledger_names_cte.c.alias_code, 
                                               cast(func.sum(TallyPurchase.credit), 
                                                    DECIMAL(10, 2)).label("tally_purchase_amt")))

        # Query to fetch tally purchase return data
        tally_purchasereturn_query = (self.Session.query(TallyPurchaseReturn.date, TallyPurchaseReturn.particulars, 
                                                         cast(func.sum(TallyPurchaseReturn.debit), 
                                                              DECIMAL(10, 2)).label("tally_purchasereturn_amt"), 
                                                        distinct_ledger_names_cte.c.alias_code)
                                    .outerjoin(distinct_ledger_names_cte, 
                                               TallyPurchaseReturn.particulars == distinct_ledger_names_cte.c.ledger)
                                    .filter(TallyPurchaseReturn.date.between(fromdate_dt, todate_dt), 
                                            distinct_ledger_names_cte.c.alias_code != 'None')
                                    .group_by(distinct_ledger_names_cte.c.alias_code)
                                    .order_by(distinct_ledger_names_cte.c.alias_code)
                                    .with_entities(distinct_ledger_names_cte.c.alias_code, 
                                                   cast(func.sum(TallyPurchaseReturn.debit), 
                                                        DECIMAL(10, 2)).label("tally_purchasereturn_amt")))

        # Calculate tally receipts amount
        tally_receipts_amt = (cast(func.sum(
                    case((TallyReceipts.amount_type == 'credit', TallyReceipts.amount), else_=0)), 
                    DECIMAL(10, 2)) - 
                            cast(func.sum(
                    case((TallyReceipts.amount_type == 'debit', TallyReceipts.amount), else_=0)), 
                    DECIMAL(10, 2))).label("tally_receipts_amt")

        # Query to fetch tally receipts data
        tally_receipts_query = (self.Session.query(TallyReceipts.date, TallyReceipts.particulars, 
                                                   tally_receipts_amt, distinct_ledger_names_cte.c.alias_code)
                                .outerjoin(distinct_ledger_names_cte, 
                                           TallyReceipts.particulars == distinct_ledger_names_cte.c.ledger)
                                .filter(TallyReceipts.date.between(fromdate_dt, todate_dt), 
                                        distinct_ledger_names_cte.c.alias_code != 'None')
                                .group_by(distinct_ledger_names_cte.c.alias_code)
                                .with_entities(distinct_ledger_names_cte.c.alias_code, tally_receipts_amt))

        # Calculate tally payments amount
        tally_payments_amt = (cast(func.sum(
                    case((TallyPayment.amount_type == 'debit', TallyPayment.amount), else_=0)), 
                    DECIMAL(10, 2)) - 
                            cast(func.sum(
                    case((TallyPayment.amount_type == 'credit', TallyPayment.amount), else_=0)), 
                    DECIMAL(10, 2))).label("tally_payments_amt")

        # Query to fetch tally payments data
        tally_payments_query = (self.Session.query(TallyPayment.date, TallyPayment.particulars, 
                                                   tally_payments_amt, distinct_ledger_names_cte.c.alias_code)
                                .outerjoin(distinct_ledger_names_cte, 
                                           TallyPayment.particulars == distinct_ledger_names_cte.c.ledger)
                                .filter(TallyPayment.date.between(fromdate_dt, todate_dt), 
                                        distinct_ledger_names_cte.c.alias_code != 'None')
                                .group_by(distinct_ledger_names_cte.c.alias_code)
                                .order_by(distinct_ledger_names_cte.c.alias_code)
                                .with_entities(distinct_ledger_names_cte.c.alias_code, tally_payments_amt))

        # Calculate tally journal amount
        tally_journal_amt = (cast(func.sum(
                    case((TallyJournal.amount_type == 'debit', TallyJournal.amount), else_=0)), 
                    DECIMAL(10, 2)) - 
                            cast(func.sum(
                    case((TallyJournal.amount_type == 'credit', TallyJournal.amount), else_=0)), 
                    DECIMAL(10, 2))).label("tally_journal_amt")

        # Query to fetch tally journal data
        tally_journal_query = (self.Session.query(TallyJournal.date, TallyJournal.particulars, 
                                                  tally_journal_amt, distinct_ledger_names_cte.c.alias_code)
                            .outerjoin(distinct_ledger_names_cte, 
                                       TallyJournal.particulars == distinct_ledger_names_cte.c.ledger)
                            .filter(TallyJournal.date.between(fromdate_dt, todate_dt), 
                                    distinct_ledger_names_cte.c.alias_code != 'None')
                            .group_by(distinct_ledger_names_cte.c.alias_code)
                            .order_by(distinct_ledger_names_cte.c.alias_code)
                            .with_entities(distinct_ledger_names_cte.c.alias_code, tally_journal_amt))

        # Convert query results to DataFrames
        busy_acc_df = pd.DataFrame(busy_acc_query, columns=['particulars', 'alias'])
        busy_sales_df = pd.DataFrame(busy_sales_query, columns=['alias', 'sales'])
        tally_outstanding_df = pd.DataFrame(tally_outstanding_query, columns=['alias', 'outstanding_balance'])
        tally_salesreturn_df = pd.DataFrame(tally_salesreturn_query, columns=['alias', 'credit_note'])
        tally_purchase_df = pd.DataFrame(tally_purchase_query, columns=['alias', 'purchase'])
        tally_purchasereturn_df = pd.DataFrame(tally_purchasereturn_query, columns=['alias', 'debit_note'])
        tally_receipts_df = pd.DataFrame(tally_receipts_query, columns=['alias', 'receipts'])
        tally_payments_df = pd.DataFrame(tally_payments_query, columns=['alias', 'payments'])
        tally_journal_df = pd.DataFrame(tally_journal_query, columns=['alias', 'journal'])

        # Check if tally outstanding DataFrame is not empty
        if not tally_outstanding_df.empty:
            # Merge DataFrames on 'alias' column
            joined_df = (busy_acc_df.merge(tally_outstanding_df, how='left', on=['alias'])
                        .merge(busy_sales_df, how='left', on=['alias'])
                        .merge(tally_salesreturn_df, how='left', on=['alias'])
                        .merge(tally_purchase_df, how='left', on=['alias'])
                        .merge(tally_purchasereturn_df, how='left', on=['alias'])
                        .merge(tally_receipts_df, how='left', on=['alias'])
                        .merge(tally_payments_df, how='left', on=['alias'])
                        .merge(tally_journal_df, how='left', on=['alias']))

            # Replace NaN values with 0
            joined_df.fillna(0, inplace=True)
            
            # Add 'date' column
            joined_df['date'] = todate_dt
            
            # Calculate 'balance' column
            joined_df['balance'] = (joined_df['sales'] - joined_df['credit_note'] - joined_df['purchase'] + 
                                    joined_df['debit_note'] - joined_df['receipts'] + joined_df['payments'] + 
                                    joined_df['journal'] + joined_df['outstanding_balance'])
            integer_columns = ['sales', 'credit_note', 'purchase', 'debit_note', 'balance', 
                               'receipts', 'payments', 'journal', 'outstanding_balance']
            for column in integer_columns:
                joined_df[column] = pd.to_numeric(joined_df[column])

            # Export data to an Excel file if required
            if to_export:
                if filename:
                    file_location = os.path.join(export_location, filename + ".xlsx")
                    joined_df.to_excel(file_location, index=False)
                    logger.info(f"Debtors Balance from {fromdate} to {todate} exported to {file_location} with the name of {filename}")
                else:
                    logger.critical(f"Filename not provided!")
            
            
            # Import data into the database if required
            if to_import:
                self.truncate_table(table_name='debtors_balance', commit=commit)
                self.manual_import_data(table_name='debtors_balance', df=joined_df, commit=commit)
            else:
                return logger.info(f"Debtors balance data not imported into the database as per the argument passed.")

        else:
            return logger.critical(f"Outstanding balance of {todate} is not in the database.")

        

    def intersite_reco(self, fromdate:str, todate:str, 
                       exceptions:list = None) -> pd.DataFrame:
        
        particulars = {'Kay Bee Bio-Organics Pvt Ltd OD21': 'Khordha', 
                           'Kay Bee Bio Organics Pvt Ltd MH27': 'Phaltan', 
                           'Kay Bee Bio-Organics Pvt Ltd KA29': 'Hubli', 
                           'Kay Bee Bio-Organics Pvt Ltd MP23': 'CNFIndore', 
                           'Kay Bee Bio-Organics Pvt Ltd TEL36': 'Hyderabad', 
                           'Kay Bee Bio-Organics Pvt Ltd CG22 New': 'Raipur', 
                           'Kay Bee Bio-Organics Pvt Ltd RJ08': 'Jaipur', 
                           'Kay Bee Bio-Organics Pvt Ltd PNB03': 'Bathinda', 
                           'Kay Bee Bio Organics Pvt Ltd HR06': 'Karnal', 
                           'Kay Bee Bio-Organics Pvt Ltd UP09': 'Lucknow', 
                        #    'Kay Bee Exports Phaltan': 'Phaltan', 
                           'Green Era Agri World Private Limited': 'GE Pune', 
                        #    'Kay Bee Exports International P Ltd Naga': '', 
                           'Kay Bee Bio-Organics Pvt Ltd AP37': 'Vijayawada', 
                           'Kay Bee Agri Solution Pvt Ltd MH27': 'AS Phaltan', 
                           'Kay Bee Bio-Organics Pvt Ltd GJ24': 'Gujarat', 

                           }
        excluded_particulars = ['Kay Bee Exports Phaltan', 
                                'Kay Bee Exports International P Ltd Naga',
                                    ]
        
        def busy_mitp_reco():
            
            received_mc = case(
                        *[(MITPKBBIO.particulars == key, value) for key, value in particulars.items()],
                                    else_='Unknown'
                                ).label('Received Material Centre')
            
            mitp_query = (self.Session.query(MITPKBBIO.date.label('MITP Date'), 
                                             MITPKBBIO.voucher_no.label('MITP Voucher No'), 
                                             MITPKBBIO.particulars.label('MITP Particulars'), 
                                             MITPKBBIO.item_details.label('MITP Item'), 
                                             MITPKBBIO.material_centre.label('MITP Material Centre'), 
                                             MITPKBBIO.alt_qty.label('MITP Qty'), 
                                             MITPKBBIO.alt_unit.label('MITP Unit'), received_mc, 
                                            SalesKBBIO.voucher_no.label('Sales Voucher No'))
                                .outerjoin(SalesKBBIO, 
                                            MITPKBBIO.voucher_no == SalesKBBIO.dc_no)    
                                .filter(and_(MITPKBBIO.party_type == 'Inter-Branch'), 
                                        MITPKBBIO.date.between(fromdate, todate),
                                        ~MITPKBBIO.particulars.in_(excluded_particulars)))
            
            mrfp_query = (self.Session.query(MRFPKBBIO.particulars, 
                                            MRFPKBBIO.voucher_no, MRFPKBBIO.item_details, 
                                            MRFPKBBIO.alt_qty, MRFPKBBIO.alt_unit, 
                                            MRFPKBBIO.material_centre)
                        .filter(and_(
                                MRFPKBBIO.date.between(fromdate, todate), 
                                ~MRFPKBBIO.particulars.in_(excluded_particulars), 
                                or_(
                                    MRFPKBBIO.particulars.like('Kay Bee%'),
                                    MRFPKBBIO.particulars.like('Green Era%')
                                ))
                        ))
            
            mitp_df = pd.DataFrame(mitp_query)
            mrfp_df = pd.DataFrame(mrfp_query)

            result_df = mitp_df.merge(mrfp_df, how= 'left', 
                                      left_on= ['Sales Voucher No',  
                                                'MITP Item', 'MITP Qty', 'MITP Unit', ], 
                                      right_on= ['voucher_no', 
                                                 'item_details', 'alt_qty', 'alt_unit', ])
            return print(result_df.info())
        
        def busy_mrfp_reco():

            received_mc = case(
                        *[(MITPKBBIO.particulars == key, value) for key, value in particulars.items()],
                                    else_='Unknown'
                                ).label('Received Material Centre')
            
            mitp_query = (self.Session.query(MITPKBBIO.date.label('MITP Date'), 
                                             MITPKBBIO.voucher_no.label('MITP Voucher No'), 
                                             MITPKBBIO.particulars.label('MITP Particulars'), 
                                             MITPKBBIO.item_details.label('MITP Item'), 
                                             MITPKBBIO.material_centre.label('MITP Material Centre'), 
                                             MITPKBBIO.alt_qty.label('MITP Qty'), 
                                             MITPKBBIO.alt_unit.label('MITP Unit'), received_mc, 
                                            SalesKBBIO.voucher_no.label('Sales Voucher No'))
                                .outerjoin(SalesKBBIO, 
                                            MITPKBBIO.voucher_no == SalesKBBIO.dc_no)    
                                .filter(and_(MITPKBBIO.date.between(fromdate, todate), 
                                             MITPKBBIO.party_type == 'Inter-Branch'), 
                                        ~MITPKBBIO.particulars.in_(excluded_particulars)))
            
            mrfp_query = (self.Session.query(MRFPKBBIO.particulars, 
                                            MRFPKBBIO.voucher_no, MRFPKBBIO.item_details, 
                                            MRFPKBBIO.alt_qty, MRFPKBBIO.alt_unit, 
                                            MRFPKBBIO.material_centre)
                                      .filter(and_(
                                                MRFPKBBIO.date.between(fromdate, todate), 
                                                ~MRFPKBBIO.particulars.in_(excluded_particulars), 
                                                or_(
                                                    MRFPKBBIO.particulars.like('Kay Bee%'),
                                                    MRFPKBBIO.particulars.like('Green Era%')
                                                ))
                                        ))
            
            mitp_df = pd.DataFrame(mitp_query)
            mrfp_df = pd.DataFrame(mrfp_query)

            result_df = mrfp_df.merge(mitp_df, how= 'left', 
                                      right_on= ['Sales Voucher No',  
                                                'MITP Item', 'MITP Qty', 'MITP Unit', ], 
                                      left_on= ['voucher_no', 
                                                 'item_details', 'alt_qty', 'alt_unit', ])

            return print(result_df.info())

        busy_mitp_reco()
        busy_mrfp_reco()    



