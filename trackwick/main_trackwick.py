from trackwick import api_data
from Database.sql_connector import kbbio_engine, kbbio_connector
from Database.models.base import KBBIOBase
from Database.db_crud import DatabaseCrud
from logging_config import logger
from datetime import datetime, timedelta
import pandas as pd


# today = datetime.today().date().strftime("%Y-%m-%d")
today = '2025-01-01'
expense_from_date = (datetime.today().date() - timedelta(days=30)).strftime("%Y-%m-%d")
expense_to_date = datetime.today().date().strftime("%Y-%m-%d")


def import_employees(): 
    start_date = today
    end_date = start_date
    table = 'trackwick_employees'
    try:
        df = api_data.api_employees(start_date=start_date, end_date=end_date)
        logger.info(f"Employee data fetched successfully: {df.shape[0]} rows, {df.shape[1]} columns.")
        
        KBBIOBase.metadata.create_all(kbbio_engine)
        db_crud = DatabaseCrud(kbbio_connector)
        
        # Delete existing data in the specified date range
        logger.info(f"Truncating '{table}'...")
        db_crud.truncate_table(table_name=table, commit=True)
        logger.info(f"'{table}' truncated.")
        
        db_crud.import_data(table, df, commit=True)
        logger.info(f"Data import completed successfully. {df.shape[0]} rows inserted into '{table}'.")
    
    except Exception as e:
        logger.error(f"Error occurred during employee import: {str(e)}")
        raise


def import_sub_dealer_liquidation_tasks(): 
    start_date = today
    end_date = start_date
    table = 'trackwick_sub_dealer_liquidation_tasks'
    try:
        df = api_data.api_sub_dealer_liquidation_tasks(start_date=start_date, end_date=end_date)
        logger.info(f"Sub Dealer Liquidation Tasks fetched successfully: {df.shape[0]} rows, {df.shape[1]} columns.")
        
        KBBIOBase.metadata.create_all(kbbio_engine)
        db_crud = DatabaseCrud(kbbio_connector)
        
        # Delete existing data in the specified date range
        db_crud.delete_date_range_query(table_name=table, 
                                        start_date= start_date, 
                                        end_date= end_date, commit=True)
        logger.info(f"Deleted Sub Dealer Liquidation Tasks from {start_date} to {end_date}....")
        
        if not df.empty:
            db_crud.import_data(table, df, commit=True)
            logger.info(f"Data import completed successfully. {df.shape[0]} rows inserted into '{table}'.")
        else: 
            logger.warning(f"No Data found from api for sub dealer liquidation tasks.")

    except Exception as e:
        logger.error(f"Error occurred during employee import: {str(e)}")
        raise


def import_farmer_liquidation_tasks(): 
    start_date = today
    end_date = start_date
    table = 'trackwick_farmer_liquidation_tasks'
    try:
        df = api_data.api_farmer_liquidation_tasks(start_date=start_date, end_date=end_date)
        logger.info(f"Farmer Liquidation Tasks fetched successfully: {df.shape[0]} rows, {df.shape[1]} columns.")
        
        KBBIOBase.metadata.create_all(kbbio_engine)
        db_crud = DatabaseCrud(kbbio_connector)
        
        # Delete existing data in the specified date range
        db_crud.delete_date_range_query(table_name=table, 
                                        start_date= start_date, 
                                        end_date= end_date, commit=True)
        logger.info(f"Deleted Farmer Liquidation Tasks from {start_date} to {end_date}....")
        
        if not df.empty:
            db_crud.import_data(table, df, commit=True)
            logger.info(f"Data import completed successfully. {df.shape[0]} rows inserted into '{table}'.")
        else:
            logger.warning(f"No Data found from api for farmer liquidation tasks.")    
    except Exception as e:
        logger.error(f"Error occurred during employee import: {str(e)}")
        raise


def import_dealer_collection_tasks(): 
    start_date = today
    end_date = start_date
    table = 'trackwick_dealer_collection_tasks'
    try:
        df = api_data.api_dealer_collection_tasks(start_date=start_date, end_date=end_date)
        logger.info(f"Dealer Collection Tasks fetched successfully: {df.shape[0]} rows, {df.shape[1]} columns.")
        
        KBBIOBase.metadata.create_all(kbbio_engine)
        db_crud = DatabaseCrud(kbbio_connector)
        
        # Delete existing data in the specified date range
        db_crud.delete_date_range_query(table_name=table, 
                                        start_date= start_date, 
                                        end_date= end_date, commit=True)
        logger.info(f"Deleted Dealer Collection Tasks from {start_date} to {end_date}....")
        
        if not df.empty:
            db_crud.import_data(table, df, commit=True)
            logger.info(f"Data import completed successfully. {df.shape[0]} rows inserted into '{table}'.")
        else:
            logger.warning(f"No Data found from api for dealer collection tasks.")
    except Exception as e:
        logger.error(f"Error occurred during employee import: {str(e)}")
        raise


def import_dealer_sales_order_tasks(): 
    start_date = today
    end_date = start_date
    table = 'trackwick_dealer_sales_order_tasks'
    try:
        df = api_data.api_dealer_sales_order_tasks(start_date=start_date, end_date=end_date)
        logger.info(f"Dealer Sales Order Tasks fetched successfully: {df.shape[0]} rows, {df.shape[1]} columns.")
        
        KBBIOBase.metadata.create_all(kbbio_engine)
        db_crud = DatabaseCrud(kbbio_connector)
        
        # Delete existing data in the specified date range
        db_crud.delete_date_range_query(table_name=table, 
                                        start_date= start_date, 
                                        end_date= end_date, commit=True)
        logger.info(f"Deleted Dealer Sales Order Tasks from {start_date} to {end_date}....")
        
        if not df.empty:
            db_crud.import_data(table, df, commit=True)
            logger.info(f"Data import completed successfully. {df.shape[0]} rows inserted into '{table}'.")
        else:
            logger.warning(f"No Data found from api for dealer sales order tasks.")
    except Exception as e:
        logger.error(f"Error occurred during employee import: {str(e)}")
        raise


def import_feedback_tasks(): 
    start_date = today
    end_date = start_date
    table = 'trackwick_feedback_tasks'
    try:
        df = api_data.api_feedback_tasks(start_date=start_date, end_date=end_date)
        logger.info(f"Feedback Tasks fetched successfully: {df.shape[0]} rows, {df.shape[1]} columns.")
        
        KBBIOBase.metadata.create_all(kbbio_engine)
        db_crud = DatabaseCrud(kbbio_connector)
        
        # Delete existing data in the specified date range
        db_crud.delete_date_range_query(table_name=table, 
                                        start_date= start_date, 
                                        end_date= end_date, commit=True)
        logger.info(f"Deleted Feedback Tasks from {start_date} to {end_date}....")
        
        if not df.empty:
            db_crud.import_data(table, df, commit=True)
            logger.info(f"Data import completed successfully. {df.shape[0]} rows inserted into '{table}'.")
        else:
            logger.warning(f"No Data found from api for feedback tasks.")
    except Exception as e:
        logger.error(f"Error occurred during employee import: {str(e)}")
        raise


def import_car_travel_expenses(): 
    start_date = expense_from_date
    end_date = expense_to_date
    table = 'trackwick_car_travel_expense'
    try:
        df = api_data.api_car_travel_expense(start_date=start_date, end_date=end_date)
        logger.info(f"Car Travel Expenses data fetched successfully: {df.shape[0]} rows, {df.shape[1]} columns.")
        
        KBBIOBase.metadata.create_all(kbbio_engine)
        db_crud = DatabaseCrud(kbbio_connector)
        
        # Delete existing data in the specified date range
        db_crud.delete_date_range_query(table_name=table, 
                                        start_date= start_date, 
                                        end_date= end_date, commit=True)
        logger.info(f"Deleted Car Travel Expenses from {start_date} to {end_date}....")
        
        if not df.empty:
            db_crud.import_data(table, df, commit=True)
            logger.info(f"Data import completed successfully. {df.shape[0]} rows inserted into '{table}'.")
        else:
            logger.warning(f"No Data found from api for car travel expenses.")

    except Exception as e:
        logger.error(f"Error occurred during employee import: {str(e)}")
        raise


def import_bike_travel_expenses(): 
    start_date = expense_from_date
    end_date = expense_to_date
    table = 'trackwick_bike_travel_expense'
    try:
        df = api_data.api_bike_travel_expense(start_date=start_date, end_date=end_date)
        logger.info(f"Bike Travel Expenses data fetched successfully: {df.shape[0]} rows, {df.shape[1]} columns.")
        
        KBBIOBase.metadata.create_all(kbbio_engine)
        db_crud = DatabaseCrud(kbbio_connector)
        
        # Delete existing data in the specified date range
        db_crud.delete_date_range_query(table_name=table, 
                                        start_date= start_date, 
                                        end_date= end_date, commit=True)
        logger.info(f"Deleted Bike Travel Expenses from {start_date} to {end_date}....")
        
        if not df.empty:
            db_crud.import_data(table, df, commit=True)
            logger.info(f"Data import completed successfully. {df.shape[0]} rows inserted into '{table}'.")
        else:
            logger.warning(f"No Data found from api for bike travel expenses.")

    except Exception as e:
        logger.error(f"Error occurred during employee import: {str(e)}")
        raise


def import_other_travel_expenses(): 
    start_date = expense_from_date
    end_date = expense_to_date
    table = 'trackwick_other_travel_expense'
    try:
        df = api_data.api_other_travel_expense(start_date=start_date, end_date=end_date)
        logger.info(f"Other Travel Expenses data fetched successfully: {df.shape[0]} rows, {df.shape[1]} columns.")
        
        KBBIOBase.metadata.create_all(kbbio_engine)
        db_crud = DatabaseCrud(kbbio_connector)
        
        # Delete existing data in the specified date range
        db_crud.delete_date_range_query(table_name=table, 
                                        start_date= start_date, 
                                        end_date= end_date, commit=True)
        logger.info(f"Deleted Other Travel Expenses from {start_date} to {end_date}....")
        
        if not df.empty:
            db_crud.import_data(table, df, commit=True)
            logger.info(f"Data import completed successfully. {df.shape[0]} rows inserted into '{table}'.")
        else:
            logger.warning(f"No Data found from api for other travel expenses.")

    except Exception as e:
        logger.error(f"Error occurred during employee import: {str(e)}")
        raise

