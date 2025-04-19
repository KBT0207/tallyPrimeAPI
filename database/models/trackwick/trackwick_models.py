from sqlalchemy import MetaData, Column, Integer, String, Date, BigInteger, Float, DateTime, func, Time, Text
from database.models.base import KBBIOBase


metadata = MetaData()


class TrackwickEmployees(KBBIOBase):
    __tablename__ = 'trackwick_employees'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    employee_name = Column(String(255), nullable= False, index= True)
    date_of_joining = Column(Date, nullable= False)
    date_of_birth = Column(Date, nullable= True)
    type = Column(String(100), nullable= True)
    team = Column(String(100), nullable= True)
    emp_id = Column(String(100), nullable= True)
    email = Column(String(255), nullable= True)
    mobile = Column(String(255), nullable= True)
    department = Column(String(100), nullable= True)
    employment_type = Column(String(100), nullable= True)
    designation = Column(String(100), nullable= True)
    work_location = Column(String(100), nullable= True)
    employee_type = Column(String(100), nullable= True)
    cost_center = Column(String(100), nullable= True)
    gender = Column(String(30), nullable= True)
    reporting_manager_1 = Column(String(255), nullable=True)
    reporting_manager_2 = Column(String(255), nullable=True)
    employee_created_date = Column(Date, nullable=True)
    aadhar_card_number = Column(String(50), nullable=True)
    deleted_by = Column(String(255), nullable=True)
    date_of_exit = Column(Date, nullable=True)
    deleted_on = Column(String(255), nullable=True)
    date_of_leaving = Column(Date, nullable=True)
    exp_in_days = Column(Integer, nullable=True)
    status = Column(String(50), nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class TrackwickSubDealerLiquidationTasks(KBBIOBase):
    __tablename__ = 'trackwick_sub_dealer_liquidation_tasks'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    employee_name = Column(String(255), nullable= False, index= True)
    title = Column(String(100), nullable= True)
    started = Column(DateTime, nullable= True)
    completed = Column(DateTime, nullable= True)
    time_taken = Column(Time, nullable= True)
    priority = Column(String(50), nullable= True)
    status = Column(String(50), nullable= True)
    customer = Column(String(100), nullable= True)
    task_address = Column(String(255), nullable= True)
    check_in = Column(String(255), nullable= True)
    check_out = Column(String(255), nullable= True)
    accuracy = Column(Integer, nullable= True)
    task_lat_lng = Column(String(100), nullable= True)
    follow_up = Column(String(20), nullable= True)
    comment = Column(String(255), nullable= True)
    liquidation_product_group = Column(String(100), nullable= True)
    liquidation_in_litres = Column(Integer, nullable= True)
    total_litres = Column(Integer, nullable= True)
    pictures = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class TrackwickFarmerLiquidationTasks(KBBIOBase):
    __tablename__ = 'trackwick_farmer_liquidation_tasks'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    employee_name = Column(String(255), nullable= False, index= True)
    title = Column(String(100), nullable= True)
    started = Column(DateTime, nullable= True)
    completed = Column(DateTime, nullable= True)
    time_taken = Column(Time, nullable= True)
    priority = Column(String(50), nullable= True)
    status = Column(String(50), nullable= True)
    customer = Column(String(100), nullable= True)
    task_address = Column(String(255), nullable= True)
    check_in = Column(String(255), nullable= True)
    check_out = Column(String(255), nullable= True)
    accuracy = Column(Integer, nullable= True)
    task_lat_lng = Column(String(100), nullable= True)
    follow_up = Column(String(20), nullable= True)
    comment = Column(String(255), nullable= True)
    liquidation_product_group = Column(String(100), nullable= True)
    liquidation_in_litres = Column(Integer, nullable= True)
    total_litres = Column(Integer, nullable= True)
    pictures = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class TrackwickDealerCollectionTasks(KBBIOBase):
    __tablename__ = 'trackwick_dealer_collection_tasks'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)    
    employee_name = Column(String(255), nullable= False, index= True)
    title = Column(String(100), nullable= True)
    started = Column(DateTime, nullable= True)
    completed = Column(DateTime, nullable= True)
    time_taken = Column(Time, nullable= True)
    priority = Column(String(50), nullable= True)
    status = Column(String(50), nullable= True)
    customer = Column(String(100), nullable= True)
    task_address = Column(String(255), nullable= True)
    check_in = Column(String(255), nullable= True)
    check_out = Column(String(255), nullable= True)
    accuracy = Column(Integer, nullable= True)
    task_lat_lng = Column(String(100), nullable= True)
    follow_up = Column(String(20), nullable= True)
    comment = Column(String(255), nullable= True)
    collection_type = Column(String(100), nullable= True)
    remittance_method = Column(String(100), nullable= True)
    amount = Column(Integer, nullable= True)
    image_attachment = Column(String(10), nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class TrackwickDealerSalesOrderTasks(KBBIOBase):
    __tablename__ = 'trackwick_dealer_sales_order_tasks'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)    
    employee_name = Column(String(255), nullable= False, index= True)
    title = Column(String(100), nullable= True)
    started = Column(DateTime, nullable= True)  
    completed = Column(DateTime, nullable= True)
    time_taken = Column(Time, nullable= True)
    priority = Column(String(50), nullable= True)
    status = Column(String(50), nullable= True)
    customer = Column(String(100), nullable= True)
    task_address = Column(String(255), nullable= True)
    check_in = Column(String(255), nullable= True)
    check_out = Column(String(255), nullable= True)
    accuracy = Column(Integer, nullable= True)
    task_lat_lng = Column(String(100), nullable= True)
    follow_up = Column(String(20), nullable= True)
    comment = Column(String(255), nullable= True)
    item_name = Column(String(150), nullable= True)
    item_quantity = Column(Integer, nullable= True)
    total_quantity = Column(Integer, nullable= True)
    pictures = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class TrackwickFeedbackTasks(KBBIOBase):
    __tablename__ = 'trackwick_feedback_tasks'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)    
    employee_name = Column(String(255), nullable= False, index= True)
    title = Column(String(100), nullable= True)
    started = Column(DateTime, nullable= True)  
    completed = Column(DateTime, nullable= True)
    time_taken = Column(Time, nullable= True)
    priority = Column(String(50), nullable= True)
    status = Column(String(50), nullable= True)
    customer = Column(String(100), nullable= True)
    task_address = Column(String(255), nullable= True)
    check_in = Column(String(255), nullable= True)
    check_out = Column(String(255), nullable= True)
    accuracy = Column(Integer, nullable= True)
    task_lat_lng = Column(String(100), nullable= True)
    follow_up = Column(String(20), nullable= True)
    comment = Column(String(255), nullable= True)
    geo = Column(String(255), nullable= True)
    visit_type = Column(String(100), nullable= True)
    visit_reason = Column(String(100), nullable= True)
    pictures = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class TrackwickCarTravelExpenses(KBBIOBase):
    __tablename__ = 'trackwick_car_travel_expense'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False) 
    employee_name = Column(String(255), nullable= False, index= True)
    emp_id = Column(String(50), nullable= False)
    form_id = Column(String(50), nullable= False)
    title = Column(String(255), nullable= False)
    description = Column(Text, nullable= True)
    status = Column(String(100), nullable= True)
    claimed = Column(Integer, nullable= False)
    approved = Column(Integer, nullable= False)
    comment = Column(String(255), nullable= True)
    start_reading = Column(Integer, nullable= True)
    end_reading = Column(Integer, nullable= True)
    total_kms_claimed = Column(Integer, nullable= True)
    rate_per_km = Column(Integer, nullable= True)
    total_amount = Column(Integer, nullable= True)
    bill_pictures = Column(Integer, nullable= True)
    
    created_at = Column(DateTime, server_default=func.now())


class TrackwickBikeTravelExpenses(KBBIOBase):
    __tablename__ = 'trackwick_bike_travel_expense'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False) 
    employee_name = Column(String(255), nullable= False, index= True)
    emp_id = Column(String(50), nullable= False)
    form_id = Column(String(50), nullable= False)
    title = Column(String(255), nullable= False)
    description = Column(Text, nullable= True)
    status = Column(String(100), nullable= True)
    claimed = Column(Integer, nullable= False)
    approved = Column(Integer, nullable= False)
    comment = Column(String(255), nullable= True)
    start_reading = Column(Integer, nullable= True)
    end_reading = Column(Integer, nullable= True)
    total_kms_claimed = Column(Integer, nullable= True)
    rate_per_km = Column(Integer, nullable= True)
    total_amount = Column(Integer, nullable= True)
    bill_pictures = Column(Integer, nullable= True)
    
    created_at = Column(DateTime, server_default=func.now())


class TrackwickOtherTravelExpenses(KBBIOBase):
    __tablename__ = 'trackwick_other_travel_expense'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False) 
    employee_name = Column(String(255), nullable= False, index= True)
    emp_id = Column(String(50), nullable= False)
    form_id = Column(String(50), nullable= False)
    title = Column(String(255), nullable= False)
    description = Column(Text, nullable= True)
    status = Column(String(100), nullable= True)
    claimed = Column(Integer, nullable= False)
    approved = Column(Integer, nullable= False)
    comment = Column(String(255), nullable= True)
    journey = Column(String(100), nullable= True)
    area_name = Column(String(255), nullable= True)
    da = Column(Integer, nullable= True)
    food_allowance = Column(Integer, nullable= True)
    accomodation = Column(Integer, nullable= True)
    other_expense = Column(Integer, nullable= True)
    total_amount = Column(Integer, nullable= True)
    bill_pictures = Column(Integer, nullable= True)
    
    created_at = Column(DateTime, server_default=func.now())
