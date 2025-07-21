from sqlalchemy import MetaData, Column, Integer, String, Date, BigInteger, Float, DateTime, func, DECIMAL
from database.models.base import KBEBase


metadata = MetaData()


class TallySalesDetailed(KBEBase):
    __tablename__ = 'tally_sales_detailed'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    date = Column(Date, nullable=False)
    voucher_no = Column(String(100), nullable=False)
    bill_ref_no = Column(String(255), nullable=False)
    voucher_type = Column(String(100), nullable=False)
    particulars = Column(String(255), nullable=False)

    item = Column(String(255), nullable=False)
    qty = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)
    rate = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    discount = Column(Float, nullable=True)

    cgst_amt = Column(Float, nullable=False)
    sgst_amt = Column(Float, nullable=False)
    igst_amt = Column(Float, nullable=False)
    
    freight_amt = Column(Float, nullable=False)
    dca_amt = Column(Float, nullable=False)
    cf_amt = Column(Float, nullable=False)

    other_amt = Column(Float, nullable=False)
    total_amt = Column(Float, nullable=False)

    material_centre = Column(String(50), nullable=False)
    currency = Column(String(50), nullable=True)
    fcy = Column(String(50), nullable=False)
    
    despatch_doc_no = Column(String(500), nullable=True)
    port_of_loading = Column(String(500), nullable=True)
    port_of_discharge = Column(String(500), nullable=True)
    narration = Column(String(600), nullable=True)
    
    created_at = Column(DateTime, server_default=func.now())

class TallySalesReturnDetailed(KBEBase):
    __tablename__ = 'tally_sales_return_detailed'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    date = Column(Date, nullable=False)
    voucher_no = Column(String(100), nullable=False)
    bill_ref_no = Column(String(255), nullable=False)
    voucher_type = Column(String(100), nullable=False)
    particulars = Column(String(255), nullable=False)

    item = Column(String(255), nullable=False)
    qty = Column(Float, nullable=False, default=0)
    unit = Column(String(50), nullable=False)
    rate = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    discount = Column(Float, nullable=True)

    cgst_amt = Column(Float, nullable=False)
    sgst_amt = Column(Float, nullable=False)
    igst_amt = Column(Float, nullable=False)
    
    freight_amt = Column(Float, nullable=False)
    dca_amt = Column(Float, nullable=False)
    cf_amt = Column(Float, nullable=False)

    other_amt = Column(Float, nullable=False)
    total_amt = Column(Float, nullable=False)

    material_centre = Column(String(50), nullable=False)
    currency = Column(String(50), nullable=True)
    fcy = Column(String(50), nullable=False)

    narration = Column(String(600), nullable=True)
    
    created_at = Column(DateTime, server_default=func.now())

class TallyPurchaseDetailed(KBEBase):
    __tablename__ = 'tally_purchase_detailed'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    date = Column(Date, nullable=False)
    voucher_no = Column(String(100), nullable=False)
    voucher_type = Column(String(100), nullable=False)
    particulars = Column(String(255), nullable=False)
    party_gstin = Column(String(50), nullable=True)

    item = Column(String(255), nullable=False)
    unit = Column(String(50), nullable=False)
    qty = Column(Float, nullable=False)
    rate = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    
    cgst_amt = Column(Float, nullable=False)
    sgst_amt = Column(Float, nullable=False)
    igst_amt = Column(Float, nullable=False)
    discount = Column(Float, nullable=False)

    freight_amt = Column(Float, nullable=False)
    dca_amt = Column(Float, nullable=False)
    cf_amt = Column(Float, nullable=False)

    other_amt = Column(Float, nullable=False)
    total_amt = Column(Float, nullable=False)

    material_centre = Column(String(50), nullable=False)
    currency = Column(String(10), nullable=True)
    fcy = Column(String(50), nullable=False)
    narration = Column(String(600), nullable=True)

    created_at = Column(DateTime, server_default=func.now())

class TallyPurchaseReturnDetailed(KBEBase):
    __tablename__ = 'tally_purchase_return_detailed'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    date = Column(Date, nullable=False)
    voucher_no = Column(String(100), nullable=False)
    voucher_type = Column(String(100), nullable=False)
    particulars = Column(String(255), nullable=False)
    party_gstin = Column(String(50), nullable=True)

    item = Column(String(255), nullable=False)
    unit = Column(String(50), nullable=False)
    qty = Column(Float, nullable=False)
    rate = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    
    cgst_amt = Column(Float, nullable=False)
    sgst_amt = Column(Float, nullable=False)
    igst_amt = Column(Float, nullable=False)

    freight_amt = Column(Float, nullable=False)
    dca_amt = Column(Float, nullable=False)
    cf_amt = Column(Float, nullable=False)

    other_amt = Column(Float, nullable=False)
    total_amt = Column(Float, nullable=False)

    material_centre = Column(String(50), nullable=False)
    currency = Column(String(10), nullable=True)
    fcy = Column(String(50), nullable=False)
    narration = Column(String(600), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    
class TallyMasters(KBEBase):
    __tablename__ = 'tally_masters'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    party_name = Column(String(255), nullable=False)
    party_alias = Column(String(255), nullable=True)
    parent = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    address_2 = Column(String(255), nullable=True)
    address_3 = Column(String(255), nullable=True)
    address_4 = Column(String(255), nullable=True)
    state = Column(String(255), nullable=True)
    country = Column(String(255), nullable=True)
    pin_code = Column(String(255), nullable=True)
    pan = Column(String(255), nullable=True)
    registration_type = Column(String(255), nullable=True)
    gstin = Column(String(40), nullable=True)
    contact_person = Column(String(255), nullable=True)
    mobile = Column(String(255), nullable=True)
    phone_no = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    email_cc = Column(String(255), nullable=True)
    credit_period = Column(String(255), nullable=True)
    material_centre = Column(String(255), nullable=False)
    fcy = Column(String(10), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class TallyItems(KBEBase):
    __tablename__ = 'tally_items'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    item_name = Column(String(255), nullable=False)
    item_alias = Column(String(255), nullable=True)
    parent = Column(String(255), nullable=True)
    unit = Column(String(50), nullable=False)
    cgst = Column(Float, nullable=False)
    sgst = Column(Float, nullable=False)
    igst = Column(Float, nullable=False)
    type_of_supply = Column(String(100), nullable=True)
    material_centre = Column(String(255), nullable=False)
    fcy = Column(String(10), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallyItemsMapping(KBEBase):
    __tablename__ = 'tally_item_mapping'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    item_name = Column(String(255), nullable=False)
    item_alias = Column(String(255), nullable=True)
    parent = Column(String(255), nullable=True)
    unit = Column(String(50), nullable=False)
    material_centre = Column(String(255), nullable=False)
    fcy = Column(String(10), nullable=False)
    mapping = Column(String(255), nullable=True)
    conversion = Column(Float, nullable=True)
    alt_unit = Column(String(50), nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class TallyReceipt(KBEBase):
    __tablename__ = 'tally_receipt_detailed'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    date = Column(Date,nullable=False)
    voucher_no = Column(String(255), nullable=False)
    party_name = Column(String(100),nullable=False)
    inr_amount = Column(Float,nullable=False)
    forex_amount = Column(Float,nullable=False)
    rate_of_exchange = Column(Float,nullable=False)
    amount_type = Column(String(10), nullable=False)
    currency = Column(String(10), nullable=True)
    fcy = Column(String(10), nullable=False)
    material_centre = Column(String(100), nullable=False)
    narration = Column(String(1000), nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class TallyPayments(KBEBase):
    __tablename__ = 'tally_payments_detailed'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    date = Column(Date,nullable=False)
    voucher_no = Column(String(255), nullable=False)
    party_name = Column(String(100),nullable=False)
    inr_amount = Column(Float,nullable=False)
    forex_amount = Column(Float,nullable=False)
    rate_of_exchange = Column(Float,nullable=True)
    amount_type = Column(String(10), nullable=False)
    currency = Column(String(10), nullable=True)
    fcy = Column(String(10), nullable=False)
    material_centre = Column(String(100), nullable=False)
    narration = Column(String(1000), nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class TallyJournal(KBEBase):
    __tablename__ = 'tally_journal_detailed'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    date = Column(Date,nullable=False)
    voucher_no = Column(String(255), nullable=False)
    party_name = Column(String(100),nullable=False)
    inr_amount = Column(Float,nullable=False)
    forex_amount = Column(Float,nullable=False)
    rate_of_exchange = Column(Float,nullable=False)
    amount_type = Column(String(10), nullable=False)
    currency = Column(String(10), nullable=True)
    fcy = Column(String(10), nullable=False)
    material_centre = Column(String(100), nullable=False)
    narration = Column(String(1000), nullable=True)
    created_at = Column(DateTime, server_default=func.now())



class TallyOutstanding(KBEBase):
    __tablename__ = 'tally_outstanding'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    voucher_no = Column(Integer, nullable=False)
    customer_name = Column(String, nullable=False)
    due_amount = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False)
    material_centre = Column(String, nullable=True)
    fcy = Column(String(10), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

