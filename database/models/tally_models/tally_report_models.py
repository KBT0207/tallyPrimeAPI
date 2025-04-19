from sqlalchemy import Column, Integer, String, DECIMAL, Float, Date, DateTime, BigInteger, func
from database.models.base import KBBIOBase



class TallySales(KBBIOBase):
    __tablename__ = 'tally_sales'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_type = Column(String(100), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    debit = Column(Float, nullable= False, default=0)
    credit = Column(Float, nullable= False, default=0)
    material_centre = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallySalesReturn(KBBIOBase):
    __tablename__ = 'tally_sales_return'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_type = Column(String(100), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    debit = Column(Float, nullable= False, default=0)
    credit = Column(Float, nullable= False, default=0)
    material_centre = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallyPurchase(KBBIOBase):
    __tablename__ = 'tally_purchase'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_type = Column(String(100), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    debit = Column(Float, nullable= False, default=0)
    credit = Column(Float, nullable= False, default=0)
    material_centre = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallyPurchaseReturn(KBBIOBase):
    __tablename__ = 'tally_purchase_return'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_type = Column(String(100), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    debit = Column(Float, nullable= False, default=0)
    credit = Column(Float, nullable= False, default=0)
    material_centre = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallyPayment(KBBIOBase):
    __tablename__ = 'tally_payments'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    material_centre = Column(String(50), nullable=False)
    amount = Column(DECIMAL(10,2), nullable=False)
    amount_type = Column(String(10), nullable=True)
    material_centre = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallyReceipts(KBBIOBase):
    __tablename__ = 'tally_receipts'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    material_centre = Column(String(50), nullable=False)
    amount = Column(DECIMAL(10,2), nullable=False)
    amount_type = Column(String(10), nullable=True)
    material_centre = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallyJournal(KBBIOBase):
    __tablename__ = 'tally_journal'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    material_centre = Column(String(50), nullable=False)
    amount = Column(DECIMAL(10,2), nullable=False)
    amount_type = Column(String(10), nullable=True)
    material_centre = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallyAccounts(KBBIOBase):
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
    created_at = Column(DateTime, server_default=func.now())



class TallyItems(KBBIOBase):
    __tablename__ = 'tally_items'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    item_name = Column(String(250), nullable= False)
    under = Column(String(100), nullable= False)
    units = Column(String(50), nullable= False)
    opening_qty = Column(DECIMAL(10,2), nullable= False)
    rate = Column(DECIMAL(10,2), nullable= False)
    per = Column(String(50), nullable= False)
    opening_balance = Column(DECIMAL(10,2), nullable=False, default=0)
    created_at = Column(DateTime, server_default=func.now())



class TallyOutstandingBalance(KBBIOBase):
    __tablename__ = 'outstanding_balance'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(250), nullable= False)
    debit = Column(DECIMAL(10,2), nullable= False)
    credit = Column(DECIMAL(10,2), nullable= False)
    material_centre = Column(String(50), nullable= False)
    created_at = Column(DateTime, server_default=func.now())



class TallyReceivables(KBBIOBase):
    __tablename__ = 'tally_receivables'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    voucher_date = Column(Date, nullable= False)
    voucher_no = Column(String(100), nullable= False)
    particulars = Column(String(250), nullable= False)
    opening_amt = Column(DECIMAL(10,2), nullable= False)
    pending_amt = Column(DECIMAL(10,2), nullable= False)
    due_date = Column(Date, nullable= False)
    overdue_days = Column(Integer, nullable= False)
    material_centre = Column(String(50), nullable= False)
    created_at = Column(DateTime, server_default=func.now())



class DebtorsBalance(KBBIOBase):
    __tablename__ = 'debtors_balance'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(250), nullable= False)
    alias = Column(String(50), nullable= False, index= True)
    outstanding_balance = Column(DECIMAL(10,2), nullable= False)
    sales = Column(DECIMAL(10,2), nullable= False)
    credit_note = Column(DECIMAL(10,2), nullable= False)
    purchase = Column(DECIMAL(10,2), nullable= False)
    debit_note = Column(DECIMAL(10,2), nullable= False)
    receipts = Column(DECIMAL(10,2), nullable= False)
    journal = Column(DECIMAL(10,2), nullable= False)
    payments = Column(DECIMAL(10,2), nullable= False)
    balance = Column(DECIMAL(10,2), nullable= False)
    created_at = Column(DateTime, server_default=func.now())



class TestTable(KBBIOBase):
    __tablename__ = 'test_table'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    ledger_name = Column(String(250), nullable= False)
    alias_code = Column(String(100), nullable= True)
    under = Column(String(100), nullable= False)
    state = Column(String(50), nullable=True)
    gst_registration_type = Column(String(100), nullable= True)
    gst_no = Column(String(100), nullable=True)
    opening_balance = Column(DECIMAL(10,2), nullable=True)
    busy_name = Column(String(250), nullable= True)
    dealer_code = Column(String(100), nullable= True)
    created_at = Column(DateTime, server_default=func.now())