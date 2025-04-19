from sqlalchemy import Column, Integer, String, Float, DateTime, func, Date
from database.models.base  import KBBIOBase
from sqlalchemy import event


class BusyPricingKBBIO(KBBIOBase):
    __tablename__ = 'busy_pricing_kbbio'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    item_name = Column(String(255), index= True, nullable=False)
    customer_type = Column(String(50), nullable= False, index=True) 
    mrp = Column(Float, nullable= False, default=0)
    selling_price = Column(Float, nullable=False, default=0)
    created_at = Column(DateTime, server_default=func.now())
    effective_from = Column(Date, nullable= False)

