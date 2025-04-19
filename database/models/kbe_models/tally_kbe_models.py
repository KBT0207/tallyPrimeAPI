from sqlalchemy import MetaData, Column, Integer, String, Date, BigInteger, Float, DateTime, func, DECIMAL
from database.models.base import KBEBase


metadata = MetaData()

class TallySales(KBEBase):
    __tablename__ = 'tally_sales'
    
    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_type = Column(String(100), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    debit = Column(Float, nullable= False, default=0)
    credit = Column(Float, nullable= False, default=0)
    material_centre = Column(String(50), nullable=False)
    currency = Column(String(50), nullable=False)
    fcy = Column(String(50),nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallySalesReturn(KBEBase):
    __tablename__ = 'tally_sales_return'
    
    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_type = Column(String(100), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    debit = Column(Float, nullable= False, default=0)
    credit = Column(Float, nullable= False, default=0)
    material_centre = Column(String(50), nullable=False)
    currency = Column(String(50), nullable=False)
    fcy = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallyPurchase(KBEBase):
    __tablename__ = 'tally_purchase'
    
    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_type = Column(String(100), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    debit = Column(Float, nullable= False, default=0)
    credit = Column(Float, nullable= False, default=0)
    material_centre = Column(String(50), nullable=False)
    currency = Column(String(50), nullable=False)
    fcy = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallyPurchaseReturn(KBEBase):
    __tablename__ = 'tally_purchase_return'
    
    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_type = Column(String(100), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    debit = Column(Float, nullable= False, default=0)
    credit = Column(Float, nullable= False, default=0)
    material_centre = Column(String(50), nullable=False)
    currency = Column(String(50), nullable=False)
    fcy = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallyPayment(KBEBase):
    __tablename__ = 'tally_payments'
    
    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    material_centre = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    amount_type = Column(String(10), nullable=True)
    material_centre = Column(String(50), nullable=False)
    currency = Column(String(50), nullable=False)
    fcy = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallyReceipts(KBEBase):
    __tablename__ = 'tally_receipts'
    
    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    material_centre = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    amount_type = Column(String(10), nullable=True)
    material_centre = Column(String(50), nullable=False)
    currency = Column(String(50), nullable=False)
    fcy = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallyJournal(KBEBase):
    __tablename__ = 'tally_journal'
    
    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    material_centre = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    amount_type = Column(String(10), nullable=True)
    material_centre = Column(String(50), nullable=False)
    currency = Column(String(50), nullable=False)
    fcy = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallyAccounts(KBEBase):
    __tablename__ = 'tally_accounts'
    
    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    ledger_name = Column(String(250), nullable= False)
    alias_code = Column(String(100), nullable= True)
    under = Column(String(100), nullable= False)
    state = Column(String(50), nullable=True)
    gst_registration_type = Column(String(100), nullable= True)
    gst_no = Column(String(100), nullable=True)
    opening_balance = Column(BigInteger, nullable=True)
    busy_name = Column(String(250), nullable= True)
    dealer_code = Column(String(100), nullable= True)
    material_centre = Column(String(50), nullable=False)
    fcy = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallyItems(KBEBase):
    __tablename__ = 'tally_items'
    
    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    item_name = Column(String(250), nullable= False)
    under = Column(String(100), nullable= False)
    units = Column(String(50), nullable= False)
    opening_qty = Column(Float, nullable= False)
    rate = Column(Float, nullable= False)
    per = Column(String(50), nullable= False)
    opening_balance = Column(Float, nullable=False, default=0)
    material_centre = Column(String(50), nullable=False)
    fcy = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())


# Tally KBE DETAILED COLS


class TallySalesDetailed(KBEBase):
    __tablename__ = 'tally_sales_detailed'
    
    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_type = Column(String(100), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    voucher_ref_no = Column(String(100), nullable= False)
    item = Column(String(255), nullable= False)
    qty = Column(Float, nullable= False, default=0)
    rate = Column(Float, nullable= False, default=0)
    rate_currency = Column(String(255), nullable= False)
    value = Column(Float, nullable= False, default=0)
    gross_total = Column(Float, nullable= False, default=0)
    other_deduction = Column(Float, nullable= False, default=0)
    material_centre = Column(String(50), nullable=False)
    fcy = Column(String(50),nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallySalesReturnDetailed(KBEBase):
    __tablename__ = 'tally_sales_return_detailed'
    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_type = Column(String(100), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    voucher_ref_no = Column(String(100), nullable= False)
    item = Column(String(255), nullable= False)
    qty = Column(Float, nullable= False, default=0)
    rate = Column(Float, nullable= False, default=0)
    rate_currency = Column(String(255), nullable= False)
    value = Column(Float, nullable= False, default=0)
    gross_total = Column(Float, nullable= False, default=0)
    material_centre = Column(String(50), nullable=False)
    fcy = Column(String(50),nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    
