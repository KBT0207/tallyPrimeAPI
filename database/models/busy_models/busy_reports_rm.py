from sqlalchemy import MetaData, Column, Integer, String, Date, BigInteger, Float, DateTime, func
from database.models.base import KBBIOBase

metadata = MetaData()


class RMPurchaseOrder(KBBIOBase):
    __tablename__ = 'busyrm_purchase_order'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    voucher_no = Column(String(255), nullable= False, index= True)
    account_group = Column(String(255), nullable= True, index= True)
    particulars = Column(String(255), nullable= False)
    item_details = Column(String(255), nullable= False)
    material_centre = Column(String(255), nullable= False)
    qty = Column(Float, nullable= False)
    unit = Column(String(10), nullable= False)
    price = Column(Float, nullable= False)
    amount = Column(Float, nullable=False)
    tax_rate = Column(String(50), nullable=True, default= 0)
    cgst_amt = Column(Float, nullable=True, default= 0)
    sgst_amt = Column(Float, nullable=True, default= 0)
    igst_amt = Column(Float, nullable=True, default= 0)
    po_value = Column(Float, nullable=True, default= 0)
    payment_term = Column(String(255), nullable= True)
    requesting_dep = Column(String(255), nullable= True)
    po_officer = Column(String(255), nullable= True)
    item_des1 = Column(String(255), nullable= True)
    item_des2 = Column(String(255), nullable= True)
    item_des3 = Column(String(255), nullable= True)
    item_des4 = Column(String(255), nullable= True)
    narration = Column(String(255), nullable= True)
    created_at = Column(DateTime, server_default=func.now())

class RMPurchaseKBBIO(KBBIOBase):
    __tablename__ = 'busyrm_purchase'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    voucher_no = Column(String(255), nullable= False, index= True)
    account_group = Column(String(255), nullable= False)
    particulars = Column(String(255), nullable= False)
    gst_no = Column(String(15), nullable= True)
    item_details = Column(String(255), nullable= False)
    batch_no = Column(String(255), nullable= True)
    batch_qty =  Column(Float(50), nullable= True)
    batch_narration =  Column(String(100), nullable= True)
    material_centre = Column(String(255), nullable= False)
    qty = Column(Float, nullable= False)
    unit = Column(String(20), nullable= False)
    price = Column(Float, nullable=False)
    amount = Column(Float, nullable=False, default= 0)
    tax_rate = Column(String(10), nullable= True)
    cgst_amt = Column(Float, nullable= True)
    sgst_amt = Column(Float, nullable= True)
    igst_amt = Column(Float, nullable= True)
    invoice_amt = Column(Float, nullable= True)
    grn_no = Column(String(255), nullable= True)
    grn_date = Column(String(50), nullable= True)
    po_number = Column(String(100), nullable=True)
    po_date = Column(String(50), nullable=True)
    type = Column(String(255), nullable=True)
    narration = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

class RMPurchaseReturnKBBIO(KBBIOBase):
    __tablename__ = 'busyrm_purchase_return'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    voucher_no = Column(String(255), nullable= False, index= True)
    particulars = Column(String(255), nullable= False)
    gst_no = Column(String(15), nullable= False)
    item_details = Column(String(255),nullable=False)
    material_centre = Column(String(255),nullable=True)
    qty = Column(Float,nullable=False)
    unit = Column(String(20),nullable=False)
    price = Column(Float(20),nullable=False)
    amount = Column(Float(20),nullable=False)
    narration = Column(String(255),nullable=True)
    created_at = Column(DateTime, server_default=func.now())

class RMStockJournal(KBBIOBase):
    __tablename__ = 'busyrm_stock_journal'

    id = Column(Integer, primary_key= True, index= True, autoincrement=True)
    date = Column(Date, nullable= False)
    voucher_no = Column(String(255), nullable= False, index=True)
    material_centre = Column(String(255), nullable= False)
    item_details = Column(String(255), nullable= True)
    batch_no = Column(String(255), nullable= True)
    batch_qty = Column(Float, nullable= False)
    batch_narration = Column(String(255), nullable= True)
    generated_qty = Column(Float, nullable= False)
    generated_unit = Column(String(10))
    generated_price = Column(Float, nullable= False) 
    
    
    
    
    
    generated_amount = Column(Float, nullable=False)
    consumed_qty = Column(Float, nullable= False)
    consumed_unit = Column(String(255))
    consumed_price = Column(Float, nullable= False) 
    consumed_amount = Column(Float, nullable=False) 
    narration = Column(String(255), nullable= True)
    plant = Column(String(255), nullable= True)
    purchase_inv = Column(String(255), nullable= True)
    created_at = Column(DateTime, server_default=func.now())

class RMStockTransfer(KBBIOBase):
    __tablename__ = 'busyrm_stock_transfer'

    id = Column(Integer, primary_key= True, index= True, autoincrement=True)
    date = Column(Date, nullable= False)
    voucher_no = Column(String(255), nullable= False, index=True)
    material_from = Column(String(255), nullable= False)
    material_to = Column(String(255), nullable= False)
    item_details = Column(String(255), nullable= True)
    batch_no = Column(String(255), nullable= True)
    batch_qty = Column(Float, nullable= True)
    batch_narration = Column(String(255), nullable= True)
    qty = Column(Float, nullable= False)
    unit = Column(String(255), nullable= False)
    price = Column(Float, nullable= False) 
    amount = Column(Float, nullable=False) 
    purchase_inv = Column(String(255), nullable= True)
    narration = Column(String(255), nullable= True)
    created_at = Column(DateTime, server_default=func.now())

class RMMRFPKBBIO(KBBIOBase):
    __tablename__ = 'busyrm_mrfp'

    id = Column(Integer, primary_key= True, index= True, autoincrement=True)
    date = Column(Date, nullable= False)
    voucher_no = Column(String(255), nullable= False, index=True)
    account_group = Column(String(255), nullable= False)
    particulars = Column(String(255), nullable= False)
    item_details = Column(String(255), nullable= False)
    batch_no = Column(String(255), nullable= True)
    batch_qty = Column(Float, nullable= True)
    batch_narration = Column(String(255), nullable= True)
    material_centre = Column(String(255), nullable= False)
    qty = Column(Float, nullable= False)
    unit = Column(String(255), nullable= False)
    price = Column(Float, nullable= False) 
    amount = Column(Float, nullable= False)
    tax_rate = Column(String(255), nullable= True)      #Alt Qty * Alt Price
    cgst_amt = Column(Float, nullable=True, default=0)
    sgst_amt = Column(Float, nullable=True, default=0)
    igst_amt = Column(Float, nullable=True, default= 0)
    grn_no = Column(String(255), nullable= True)
    grn_date = Column(String(255), nullable= True)
    po_number = Column(String(255), nullable= True)
    po_date = Column(String(255), nullable= True)
    narration = Column(String(255), nullable= True)
    created_at = Column(DateTime, server_default=func.now())

class RMMITPKBBIO(KBBIOBase):
    __tablename__ = 'busyrm_mitp'

    id = Column(Integer, primary_key= True, index= True, autoincrement=True)
    date = Column(Date, nullable= False)
    voucher_no = Column(String(255), nullable= False)
    account_group = Column(String(255), nullable= False)
    particulars = Column(String(255), nullable= False)
    product_group = Column(String(255), nullable= False)
    item_details = Column(String(255), nullable= False)
    batch_no = Column(String(255), nullable= True)
    batch_qty = Column(Float, nullable= True)
    batch_narration = Column(String(255), nullable= True)
    material_centre = Column(String(255), nullable= False)
    qty = Column(Float, nullable= False)
    unit = Column(String(255), nullable= False)
    price = Column(Float, nullable= False) 
    amount = Column(Float, nullable=False)      #Alt Qty * Alt Price
    tax_rate = Column(String(10), nullable=False)
    cgst_amt = Column(Float, nullable=True, default=0)
    sgst_amt = Column(Float, nullable=True, default=0)
    igst_amt = Column(Float, nullable=True, default= 0)
    narration = Column(String(255), nullable= True)
    created_at = Column(DateTime, server_default=func.now())

class RMProduction(KBBIOBase):
    __tablename__ = 'busyrm_production'

    id = Column(Integer, primary_key= True, index= True, autoincrement=True)
    date = Column(Date, nullable= False)
    voucher_no = Column(String(255), nullable= False, index=True)
    material_centre = Column(String(255), nullable= False)
    item_details = Column(String(255), nullable= False)
    generated_qty = Column(Float, nullable= False)
    generated_unit = Column(String(255),nullable=True,default='NA')
    batch_no = Column(String(255), nullable= True,default='NA')
    generated_price = Column(Float, nullable= False) 
    generated_amount = Column(Float, nullable=False)
    consumed_qty = Column(Float, nullable= False)
    consumed_unit = Column(String(255))
    consumed_price = Column(Float, nullable= False) 
    consumed_amount = Column(Float, nullable=False)
    narration = Column(String(255), nullable= True) 
    created_at = Column(DateTime, server_default=func.now())

