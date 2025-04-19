from trackwick.api.api_config import TrackOlapAPI
import numpy as np
import pandas as pd
from datetime import datetime


def exp_to_days_fixed(exp):
    years, months, days = 0, 0, 0
    # Split the input string into parts for parsing
    parts = exp.lower().replace("years", "year").replace("months", "month").replace("days", "day").split()
    # Iterate through the parts to extract numbers for years, months, and days
    for i, part in enumerate(parts):
        if "year" in part:
            years = int(parts[i - 1])  # The number is right before the keyword
        elif "month" in part:
            months = int(parts[i - 1])
        elif "day" in part:
            days = int(parts[i - 1])
    # Convert to total days
    return years * 365 + months * 30 + days



def api_employees(start_date:str, end_date:str) -> pd.DataFrame:
    api = TrackOlapAPI()
    active_df = api.get_report(report_id= '6769180d33821319223f3749', 
                               start_date= start_date, 
                               end_date= end_date)
    deleted_df = api.get_report(report_id= '676925be55c86f74f651ee32', 
                                start_date= start_date, 
                                end_date= end_date)
    
    def transformation(df:pd.DataFrame, status:str) -> pd.DataFrame:
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        df['exp_in_days'] = df['experience'].apply(exp_to_days_fixed)
        df = df.drop(columns= 'experience')
        df = df.rename(columns={'employee':'employee_name', 'identifier': 'emp_id', 
                                        'date_of_leaving_the_organization': 'date_of_leaving'})
        df = df.replace('NA', None)
        df['deleted_on'] = np.where(df['deleted_on'].notnull(), 
                                            df['deleted_on'].str.split(' ').str[0], None)
        
        df['date_of_leaving'] = df['date_of_leaving'].where(df['date_of_leaving'].notnull(), None)

        date_columns = ['date_of_joining', 'date_of_birth', 
                        'employee_created_date', 'date_of_exit']
        
        for column in date_columns:
            df[column] = pd.to_datetime(df[column], 
                                                dayfirst= True, 
                                                errors= 'coerce')
            df[column] = df[column].dt.strftime('%Y-%m-%d').where(df[column].notnull(), None)

        df['status'] = status
        
        return df

    employees_df = pd.concat([transformation(active_df, 'active'), 
                              transformation(deleted_df, 'deleted')], 
                              ignore_index= True )

    return employees_df


def api_sub_dealer_liquidation_tasks(start_date:str, end_date:str) -> pd.DataFrame:
    api = TrackOlapAPI()
    df = api.get_report(report_id= '676a6984338213192229a50f', 
                               start_date= start_date, 
                               end_date= end_date)

    df.columns = df.columns.str.lower().str.replace(' ', '_')
    df = df.replace('NA', None)
    df = df.drop(columns= ['type', 'start', 'delayed', 'next_follow_up_time', 'follow_up_comment'])
    df = df.rename(columns={'employee':'employee_name', 'task_lat/lng': 'task_lat_lng', 
                            'liquidation_details_-_group_of_product': 'liquidation_product_group', 
                            'liquidation_details_-_in_liters': 'liquidation_in_litres', 
                            'accuracy_%': 'accuracy', 'total_liters': 'total_litres'})
    df['date'] = start_date

    return df


def api_farmer_liquidation_tasks(start_date:str, end_date:str) -> pd.DataFrame:
    api = TrackOlapAPI()
    df = api.get_report(report_id= '676a69c633821319222a500b', 
                             start_date= start_date, 
                             end_date= end_date)

    df.columns = df.columns.str.lower().str.replace(' ', '_')
    df = df.replace('NA', None)
    df = df.drop(columns= ['type', 'start', 'delayed', 'next_follow_up_time', 'follow_up_comment'])
    df = df.rename(columns={'employee':'employee_name', 'task_lat/lng': 'task_lat_lng', 
                            'liquidation_details_-_group_of_product': 'liquidation_product_group', 
                            'liquidation_details_-_in_liters': 'liquidation_in_litres', 
                            'accuracy_%': 'accuracy', 'total_liters': 'total_litres'})
    df['date'] = start_date

    return df


def api_dealer_collection_tasks(start_date:str, end_date:str) -> pd.DataFrame:
    api = TrackOlapAPI()
    df = api.get_report(report_id= '676a6a2e55c86f74f6bbb941', 
                             start_date= start_date, 
                             end_date= end_date)

    df.columns = df.columns.str.lower().str.replace(' ', '_')
    df = df.replace('NA', None)
    df = df.drop(columns= ['type', 'start', 'delayed', 'next_follow_up_time', 'follow_up_comment'])
    df = df.rename(columns={'employee':'employee_name', 'task_lat/lng': 'task_lat_lng', 
                            'type_of_collection': 'remittance_method', 'accuracy_%': 'accuracy'})
    df['date'] = start_date

    return df


def api_dealer_sales_order_tasks(start_date:str, end_date:str) -> pd.DataFrame:
    api = TrackOlapAPI()
    df = api.get_report(report_id= '676a6a5733821319222c2542', 
                             start_date= start_date, 
                             end_date= end_date)

    df.columns = df.columns.str.lower().str.replace(' ', '_')
    df = df.replace('NA', None)
    df = df.drop(columns= ['type', 'start', 'delayed', 'next_follow_up_time', 'follow_up_comment'])
    df = df.rename(columns={'employee':'employee_name', 'task_lat/lng': 'task_lat_lng', 
                            'type_of_collection': 'remittance_method', 'accuracy_%': 'accuracy', 
                            'sales_order_form_-_product': 'item_name', 
                            'sales_order_form_-_quantity': 'item_quantity', 'attach_images': 'pictures'})
    df['date'] = start_date

    return df


def api_dealer_sales_order_tasks(start_date:str, end_date:str) -> pd.DataFrame:
    api = TrackOlapAPI()
    df = api.get_report(report_id= '676a6a5733821319222c2542', 
                             start_date= start_date, 
                             end_date= end_date)

    df.columns = df.columns.str.lower().str.replace(' ', '_')
    df = df.replace('NA', None)
    df = df.drop(columns= ['type', 'start', 'delayed', 'next_follow_up_time', 'follow_up_comment'])
    df = df.rename(columns={'employee':'employee_name', 'task_lat/lng': 'task_lat_lng', 
                            'type_of_collection': 'remittance_method', 'accuracy_%': 'accuracy', 
                            'sales_order_form_-_product': 'item_name', 
                            'sales_order_form_-_quantity': 'item_quantity', 'attach_images': 'pictures'})
    df['date'] = start_date

    return df


def api_feedback_tasks(start_date:str, end_date:str) -> pd.DataFrame:
    api = TrackOlapAPI()
    df = api.get_report(report_id= '676a6a7c55c86f74f6bc6b12', 
                             start_date= start_date, 
                             end_date= end_date)

    df.columns = df.columns.str.lower().str.replace(' ', '_')
    df = df.replace('NA', None)
    df = df.drop(columns= ['type', 'start', 'delayed', 'next_follow_up_time', 'follow_up_comment'])
    df = df.rename(columns={'employee':'employee_name', 'task_lat/lng': 'task_lat_lng', 
                            'type_of_visit': 'visit_type', 'accuracy_%': 'accuracy', 
                            'reason_of_visit': 'visit_reason', 'attach_images': 'pictures'})
    df['date'] = start_date

    return df



def api_car_travel_expense(start_date:str, end_date:str) -> pd.DataFrame:
    api = TrackOlapAPI()
    df = api.get_report(report_id= '676bd35755c86f74f683dfdb', 
                             start_date= start_date, 
                             end_date= end_date)

    df.columns = df.columns.str.lower().str.replace(' ', '_') 
    df = df.replace('NA', None)
    df = df.drop(columns= 'type')
    df = df.rename(columns={'employee':'employee_name', 'identifier': 'emp_id', 
                            'id' :'form_id', 'total_kms_(claimed)': 'total_kms_claimed', 
                            'rate_(per_km)': 'rate_per_km'})
    
    zero_columns = ['claimed', 'approved', 'start_reading', 'end_reading', 
                    'total_kms_claimed', 'rate_per_km', 'total_amount', 'bill_pictures']
    df[zero_columns] = df[zero_columns].fillna(0)
    df = df.sort_values(by= ['date', 'employee_name'])

    return df


def api_bike_travel_expense(start_date:str, end_date:str) -> pd.DataFrame:
    api = TrackOlapAPI()
    df = api.get_report(report_id= '676bd3af55c86f74f684a5ab', 
                             start_date= start_date, 
                             end_date= end_date)

    df.columns = df.columns.str.lower().str.replace(' ', '_') 
    df = df.replace('NA', None)
    df = df.drop(columns= 'type')
    df = df.rename(columns={'employee':'employee_name', 'identifier': 'emp_id', 
                            'id' :'form_id', 'total_kms_(claimed)': 'total_kms_claimed', 
                            'rate_(per_km)': 'rate_per_km'})
    
    zero_columns = ['claimed', 'approved', 'start_reading', 'end_reading', 
                    'total_kms_claimed', 'rate_per_km', 'total_amount', 'bill_pictures']
    df[zero_columns] = df[zero_columns].fillna(0)
    df = df.sort_values(by= ['date', 'employee_name'])

    return df


def api_other_travel_expense(start_date:str, end_date:str) -> pd.DataFrame:
    api = TrackOlapAPI()
    df = api.get_report(report_id= '676bd4e73382131922641cac', 
                             start_date= start_date, 
                             end_date= end_date)

    df.columns = df.columns.str.lower().str.replace(' ', '_') 
    df = df.replace('NA', None)
    df = df.drop(columns= 'type')
    df = df.rename(columns={'employee':'employee_name', 'identifier': 'emp_id', 
                            'id' :'form_id', 
                            'pictures_/_image_attachment': 'bill_pictures'})
    
    zero_columns = ['claimed', 'approved', 'other_expense', 'accomodation', 'da', 
                    'food_allowance', 'total_amount', 'bill_pictures']
    df[zero_columns] = df[zero_columns].fillna(0) 
    df = df.sort_values(by= ['date', 'employee_name'])
    return df


