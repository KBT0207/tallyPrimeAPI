from sqlalchemy import Column, Integer, String, BigInteger, Float, DateTime, func
from database.models.base  import KBBIOBase



class BusyAccountsKBBIO(KBBIOBase):
    __tablename__ = 'busy_acc_kbbio'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    name = Column(String(255), unique= True, index= True)
    alias = Column(String(100), nullable= True)
    parent_group = Column(String(255), nullable= True)
    opening_balance_credit = Column(Float, nullable= False, default=0)
    opening_balance_debit = Column(Float, nullable= False, default=0)
    dealer_type = Column(String(255), nullable= True)
    gst_no = Column(String(15), nullable= True)
    pan =  Column(String(10), nullable= True)
    filing_frequency =  Column(String(20), nullable= True)
    credit_limit = Column(Float, nullable= False, default=0)
    state = Column(String(50), nullable= True)
    address1 = Column(String(255), nullable= True)
    address2 = Column(String(255), nullable= True)
    pincode = Column(BigInteger, nullable= True)
    territory = Column(String(50), nullable= True)
    mobile_no = Column(String(50), nullable= True)
    contact_person = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    salesman = Column(String(100), nullable= True)
    email = Column(String(150), nullable= True)


class BusyAccounts100x(KBBIOBase):
    __tablename__ = 'busy_acc_100x'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    name = Column(String(255), unique= True, index= True)
    alias = Column(String(100), nullable= True)
    parent_group = Column(String(255), nullable= True)
    opening_balance_credit = Column(Float, nullable= False, default=0)
    opening_balance_debit = Column(Float, nullable= False, default=0)
    dealer_type = Column(String(255), nullable= True)
    gst_no = Column(String(15), nullable= True)
    pan =  Column(String(10), nullable= True)
    filing_frequency =  Column(String(20), nullable= True)
    credit_limit = Column(Float, nullable= False, default=0)
    state = Column(String(50), nullable= True)
    address1 = Column(String(255), nullable= True)
    address2 = Column(String(255), nullable= True)
    pincode = Column(BigInteger, nullable= True)
    territory = Column(String(50), nullable= True)
    mobile_no = Column(String(50), nullable= True)
    contact_person = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now())



class BusyAccountsGreenEra(KBBIOBase):
    __tablename__ = 'busy_acc_greenera'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    name = Column(String(255), unique= True, index= True)
    alias = Column(String(100), nullable= True)
    parent_group = Column(String(255), nullable= True)
    opening_balance_credit = Column(Float, nullable= False, default=0)
    opening_balance_debit = Column(Float, nullable= False, default=0)
    dealer_type = Column(String(255), nullable= True)
    gst_no = Column(String(15), nullable= True)
    pan =  Column(String(10), nullable= True)
    filing_frequency =  Column(String(20), nullable= True)
    credit_limit = Column(Float, nullable= False, default=0)
    state = Column(String(50), nullable= True)
    address1 = Column(String(255), nullable= True)
    address2 = Column(String(255), nullable= True)
    pincode = Column(BigInteger, nullable= True)
    territory = Column(String(50), nullable= True)
    mobile_no = Column(String(50), nullable= True)
    contact_person = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now())



class BusyAccountsAgri(KBBIOBase):
    __tablename__ = 'busy_acc_agri'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    name = Column(String(255), unique= True, index= True)
    alias = Column(String(100), nullable= True)
    parent_group = Column(String(255), nullable= True)
    opening_balance_credit = Column(Float, nullable= False, default=0)
    opening_balance_debit = Column(Float, nullable= False, default=0)
    dealer_type = Column(String(255), nullable= True)
    gst_no = Column(String(15), nullable= True)
    pan =  Column(String(10), nullable= True)
    filing_frequency =  Column(String(20), nullable= True)
    credit_limit = Column(Float, nullable= False, default=0)
    state = Column(String(50), nullable= True)
    address1 = Column(String(255), nullable= True)
    address2 = Column(String(255), nullable= True)
    pincode = Column(BigInteger, nullable= True)
    territory = Column(String(50), nullable= True)
    mobile_no = Column(String(50), nullable= True)
    contact_person = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now())



class BusyAccountsNewAge(KBBIOBase):
    __tablename__ = 'busy_acc_newage'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    name = Column(String(255), unique= True, index= True)
    alias = Column(String(100), nullable= True)
    parent_group = Column(String(255), nullable= True)
    opening_balance_credit = Column(Float, nullable= False, default=0)
    opening_balance_debit = Column(Float, nullable= False, default=0)
    dealer_type = Column(String(255), nullable= True)
    gst_no = Column(String(15), nullable= True)
    pan =  Column(String(10), nullable= True)
    filing_frequency =  Column(String(20), nullable= True)
    credit_limit = Column(Float, nullable= False, default=0)
    state = Column(String(50), nullable= True)
    address1 = Column(String(255), nullable= True)
    address2 = Column(String(255), nullable= True)
    pincode = Column(BigInteger, nullable= True)
    territory = Column(String(50), nullable= True)
    mobile_no = Column(String(50), nullable= True)
    contact_person = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now())



# raw material

class BusyAccountsKBBIORM(KBBIOBase):
    __tablename__ = 'busy_acc_kbbiorm'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    name = Column(String(255), unique= True, index= True)
    alias = Column(String(100), nullable= True)
    parent_group = Column(String(255), nullable= True)
    opening_balance_credit = Column(Float, nullable= False, default=0)
    opening_balance_debit = Column(Float, nullable= False, default=0)
    dealer_type = Column(String(255), nullable= True)
    gst_no = Column(String(15), nullable= True)
    pan =  Column(String(10), nullable= True)
    filing_frequency =  Column(String(20), nullable= True)
    credit_limit = Column(Float, nullable= False, default=0)
    state = Column(String(50), nullable= True)
    address1 = Column(String(255), nullable= True)
    address2 = Column(String(255), nullable= True)
    pincode = Column(BigInteger, nullable= True)
    territory = Column(String(50), nullable= True)
    mobile_no = Column(String(50), nullable= True)
    contact_person = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
