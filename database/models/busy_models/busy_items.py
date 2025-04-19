from sqlalchemy import Column, Integer, String, Float, DateTime, func
from database.models.base import KBBIOBase



class BusyItemsKBBIO(KBBIOBase):
    __tablename__ = 'busy_items_kbbio'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    name = Column(String(255), unique= True, index= True)
    alias = Column(String(100), nullable= True)
    parent_group = Column(String(255), nullable= True)
    opening_stock = Column(Float, nullable= False, default=0)
    unit = Column(String(30), nullable= False)
    tax_category = Column(String(50), nullable= False)
    created_at = Column(DateTime, server_default=func.now())



class BusyItems100x(KBBIOBase):
    __tablename__ = 'busy_items_100x'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    name = Column(String(255), primary_key= True, unique= True, index= True)
    alias = Column(String(100), nullable= True)
    parent_group = Column(String(255), nullable= True)
    opening_stock = Column(Float, nullable= False, default=0)
    unit = Column(String(30), nullable= False)
    tax_category = Column(String(50), nullable= False)
    created_at = Column(DateTime, server_default=func.now())



class BusyItemsNewAge(KBBIOBase):
    __tablename__ = 'busy_items_newage'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    name = Column(String(255), unique= True, index= True)
    alias = Column(String(100), nullable= True)
    parent_group = Column(String(255), nullable= True)
    opening_stock = Column(Float, nullable= False, default=0)
    unit = Column(String(30), nullable= False)
    tax_category = Column(String(50), nullable= False)
    created_at = Column(DateTime, server_default=func.now())



class BusyItemsAgri(KBBIOBase):
    __tablename__ = 'busy_items_agri'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    name = Column(String(255), unique= True, index= True)
    alias = Column(String(100), nullable= True)
    parent_group = Column(String(255), nullable= True)
    opening_stock = Column(Float, nullable= False, default=0)
    unit = Column(String(30), nullable= False)
    tax_category = Column(String(50), nullable= False)
    created_at = Column(DateTime, server_default=func.now())



class BusyItemsGreenEra(KBBIOBase):
    __tablename__ = 'busy_items_greenera'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    name = Column(String(255), unique= True, index= True)
    alias = Column(String(100), nullable= True)
    parent_group = Column(String(255), nullable= True)
    opening_stock = Column(Float, nullable= False, default=0)
    unit = Column(String(30), nullable= False)
    tax_category = Column(String(50), nullable= False)
    created_at = Column(DateTime, server_default=func.now())

