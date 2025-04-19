from sqlalchemy import Column, Integer, String, BigInteger, Float, DateTime, func
from database.models.base  import KBBIOBase

class BusyAccountsKBBIORM(KBBIOBase):
    __tablename__ = 'busyrm_acc'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    name = Column(String(255), unique= True, index= True)
    alias = Column(String(100), nullable= True)
    parent_group = Column(String(255), nullable= True)
    address1 = Column(String(255), nullable= True)
    address2 = Column(String(255), nullable= True)
    address3 = Column(String(255), nullable= True)
    state = Column(String(100),nullable=False)
    opening_balance_debit = Column(Float, nullable= False, default=0)
    opening_balance_credit = Column(Float, nullable= False, default=0)
    dealer_type = Column(String(255), nullable= True)
    gst_no = Column(String(15), nullable= True)
    filing_frequency =  Column(String(20), nullable= True)
    mobile_no = Column(String(50), nullable= True)
    created_at = Column(DateTime, server_default=func.now())