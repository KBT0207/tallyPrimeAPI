from sqlalchemy import Column, Integer, String, BigInteger, Float, DateTime, func
from database.models.base  import KBBIOBase


class BusyItemsKBBIORM(KBBIOBase):
    __tablename__ = 'busyrm_items'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    name = Column(String(255), unique= True, index= True)
    alias = Column(String(100), nullable= True)
    parent_group = Column(String(255), nullable= True)
    opening_stock = Column(Float, nullable= False, default=0)
    unit = Column(String(30), nullable= False)
    tax_category = Column(String(50), nullable= False)
    created_at = Column(DateTime, server_default=func.now())
