from sqlalchemy import MetaData, Column, Integer, String, Date, BigInteger, Float, DateTime, func
from database.models.base import KBEBase


metadata = MetaData()


class ExchangeRate(KBEBase):
    __tablename__= 'exchange_rate'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    currency = Column(String(10), nullable=False)
    exchange_rate = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class KBEOutstanding(KBEBase):
    __tablename__ = 'outstanding_balance'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    voucher_no = Column(String(255), nullable= False, index= True)
    particulars = Column(String(255), nullable= False)
    amount = Column(Float, nullable=False) 
    currency = Column(String(10), nullable=False) 
    exchange_rate = Column(Float, nullable=False)
    amount_in_INR = Column(Float, nullable=False)
    due_on = Column(Date, nullable=False)
    overdue_in_days = Column(Integer, nullable=True)
    material_centre = Column(String(50), nullable= False)
    created_at = Column(DateTime, server_default=func.now())



# class KBEAccounts(KBEBase):
#     __tablename__ = 'tally_accounts'

#     id = Column(Integer, primary_key= True, autoincrement= True, index= True)
#     ledger_name = Column(String(250), nullable= False)
#     alias_code = Column(String(100), nullable= True)
#     under = Column(String(100), nullable= False)
#     opening_balance = Column(BigInteger, nullable=True)
#     material_centre = Column(String(50), nullable=False)
#     salesman = Column(String(250), nullable= True)
#     country = Column(String(100), nullable= True)
#     credit_days = Column(Integer, nullable=False)
#     created_at = Column(DateTime, server_default=func.now())
