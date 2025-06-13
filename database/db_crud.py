import pandas as pd
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import insert, delete, and_, func, cast, select, Numeric, Table, text, MetaData, desc
from logging_config import logger
from utils.common_utils import tables
from sqlalchemy.exc import SQLAlchemyError
from database.models.kbe_models.export_models import ExchangeRate


class DatabaseCrud:
    def __init__(self, db_connector) -> None:
        self.db_connector = db_connector
        self.db_engine = db_connector.engine
        self.Session = scoped_session(sessionmaker(bind=self.db_connector.engine, autoflush=False))

    
    def delete_date_range_query(self, table_name: str, start_date: str, end_date: str, commit: bool) -> None:
        """
        Deletes rows in the specified table within the given date range.

        Args:
            table_name (str): The name of the table from which rows are to be deleted.
            start_date (str): The start date of the date range in 'YYYY-MM-DD' format.
            end_date (str): The end date of the date range in 'YYYY-MM-DD' format.
            commit (bool): Whether to commit the transaction.

        Returns:
            None
        """
        table_class = tables.get(table_name)
        if not table_class:
            logger.error(f"Table '{table_name}' not found in table mapping. Delete query failed to execute.")
            return

        if start_date > end_date:
            logger.error(f"Start date '{start_date}' should be less than or equal to end date '{end_date}'.")
            return

        date_condition = table_class.date.between(start_date, end_date)
        delete_query = delete(table_class).where(date_condition)

        try:
            with self.db_engine.connect() as connection:
                transaction = connection.begin()
                try:
                    result = connection.execute(delete_query)
                    deleted_count = result.rowcount
                    logger.info(f"Deleted {deleted_count} rows from '{table_name}' between {start_date} and {end_date}.")
                    
                    if commit:
                        transaction.commit()
                        logger.info("Transaction committed.")
                    else:
                        transaction.rollback()
                        logger.info("Transaction not committed.")
                except SQLAlchemyError as e:
                    transaction.rollback()
                    logger.error(f"Error occurred during deletion: {e}")
        except SQLAlchemyError as e:
            logger.error(f"Connection error: {e}")
        


    def get_row_count(self, table_name):
        table_class = tables.get(table_name)
        
        if not table_class:
            logger.error(f"Table '{table_name}' not found in table_mapping.")
            return None

        with self.db_engine.connect() as connection:
            if isinstance(table_class, Table):  # If it's a Table object
                count_query = select([func.count()]).select_from(table_class)
                row_count = connection.execute(count_query).scalar()
            else:  # If it's an ORM class
                table_name = table_class.__tablename__
                row_count = connection.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()

        return row_count
    
    

    def import_data(self, table_name, df: pd.DataFrame, commit):
        if df is not None:
            row_count_before = self.get_row_count(table_name)
            row_count_after = None
            
            try:
                with self.db_engine.connect() as connection:
                    df.to_sql(table_name, self.db_connector.engine, if_exists='append', index=False, method='multi', chunksize=500)
                    row_count_after = self.get_row_count(table_name)
                    if commit:
                        connection.commit()
            except SQLAlchemyError as e:
                logger.critical(f"Error inserting data into {table_name}: {e}")
                if row_count_after is not None:
                    connection.rollback()
                    logger.error(f"Rolling back changes in {table_name} due to import error.")
            except Exception as e:
                logger.critical(f"Unknown error occurred: {e}")

            if (row_count_before is not None) and (row_count_after is not None):
                rows_inserted = row_count_after - row_count_before
                logger.info(f"Data imported into {table_name}. {rows_inserted} rows inserted.")
            else:
                logger.error("Failed to determine rows inserted.")
        else:
            logger.error(f"Empty Dataframe hence 0 rows imported in {table_name}")



    def truncate_table(self, table_name: str, commit: bool) -> None:
        """
        Truncate the specified database table.

        This method deletes all rows from the specified table using SQLAlchemy's delete operation.

        Args:
            table_name (str): The name of the table to truncate.
            commit (bool): If True, commit the transaction; otherwise, roll back.

        Returns:
            None
        """
        # Retrieve table class from metadata
        table_class = tables.get(table_name)
        if table_class:
            # Prepare truncate query
            truncate_query = delete(table_class)

            try:
                with self.db_engine.connect() as connection:
                    # Execute truncate query
                    connection.execute(truncate_query)
                    if commit:
                        connection.commit()
                        logger.info(f"Table '{table_name}' truncated successfully.")
                    else:
                        connection.rollback()
                        logger.info(f"Transaction rolled back for truncating '{table_name}'.")

            except SQLAlchemyError as e:
                logger.critical(f"Error truncating table '{table_name}': {e}")
                connection.rollback()
                logger.error(f"Rolling back changes in '{table_name}' due to truncation error.")
            except Exception as e:
                logger.critical(f"Unknown error occurred while truncating '{table_name}': {e}")
                connection.rollback()
                logger.error(f"Rolling back changes in '{table_name}' due to an unknown error.")
        else:
            logger.error(f"Table '{table_name}' not found in table_mapping.")



    
        

    # def import_kbe_accounts_data(self, df:pd.DataFrame, commit:bool):
        
    #     df['ledger_name'] = df['ledger_name'].str.title()

    #     df_material_centre = df["material_centre"][1]
        
    #     accounts = self.Session.query(KBEAccounts.ledger_name, KBEAccounts.under, 
    #                                   KBEAccounts.material_centre,                                 
    #                                         ).filter(KBEAccounts.material_centre == df_material_centre)
        
    #     df_accounts = pd.DataFrame(accounts, columns=['ledger_name', 'under', 'material_centre'],)
        
    #     df_accounts['ledger_name'] = df_accounts['ledger_name'].str.title()
        
    #     if not df_accounts.empty:
    #         new_data = df.merge(df_accounts, how= 'left', on= ['ledger_name', 'under', 'material_centre'], indicator=True)
    #         new_data = (new_data.loc[new_data['_merge']=='left_only', 
    #                                 ['ledger_name', 'under', 'opening_balance', 'material_centre', 
    #                                     'alias_code', 'credit_days',
    #                                     ]])
    #         new_data['alias_code'] = new_data['alias_code'].where(pd.notna(new_data['alias_code']), None)
    #     else: 
    #         new_data = df
        
    #     if not new_data.empty: 
    #         values = new_data.to_dict('records')
    #         insert_stmt = insert(KBEAccounts).values(values)
    #         try:
    #             with self.db_engine.connect() as connection:
    #                 result = connection.execute(insert_stmt)
    #                 logger.info(f"{result.rowcount} rows inserted into tally_accounts.")
    #                 if commit:
    #                     connection.commit()
    #                     logger.info(f"Inserted {result.rowcount} rows into tally_accounts.")
    #                 else:
    #                     connection.rollback()
    #                     logger.info(f"Transaction rollback successfully without any errors as commit was given False.")
    #         except SQLAlchemyError as e:
    #             logger.critical(f"Error inserting data into tally_accounts: {e}")
    #             connection.rollback()
    #             logger.error(f"Rolling back changes in tally_accounts due to import error.")
    #         except Exception as e:
    #             logger.critical(f"Unknown error occurred: {e}")
    #     else:
    #         logger.info(f"No new data to import in the database.")
        


    # def clean_kbe_accounts_data(self, df:pd.DataFrame, commit:bool):
            
    #         df['ledger_name'] = df['ledger_name'].str.title()

    #         df_material_centre = df["material_centre"][1]
            
    #         accounts = (self.Session.query(KBEAccounts.id, KBEAccounts.ledger_name, KBEAccounts.under, 
    #                                     KBEAccounts.material_centre)
    #                                 .filter(KBEAccounts.material_centre == df_material_centre))
            
    #         df_accounts = pd.DataFrame(accounts, columns=['id', 'ledger_name', 'under', 'material_centre'],)
            
    #         df_accounts['ledger_name'] = df_accounts['ledger_name'].str.title()
            
    #         if not df.empty:
    #             new_data = df_accounts.merge(df, how= 'left', on= ['ledger_name', 'under', 'material_centre'], indicator=True)
    #             new_data = new_data.loc[new_data['_merge']=='left_only', ['id', 'ledger_name']]
    
    #         if not new_data.empty: 
    #             id_to_delete = new_data['id'].to_list()

    #             delete_query = delete(KBEAccounts).where(KBEAccounts.id.in_(id_to_delete))

    #             try:
    #                 with self.db_engine.connect() as connection:
    #                     transaction = connection.begin()
    #                     try:
    #                         result = connection.execute(delete_query)
    #                         deleted_count = result.rowcount
    #                         logger.info(f"Deleted {deleted_count} rows from KBEAccounts of ids {id_to_delete}.")
                            
    #                         if commit:
    #                             transaction.commit()
    #                             logger.info("Transaction committed.")
    #                         else:
    #                             transaction.rollback()
    #                             logger.info("Transaction not committed.")
    #                     except SQLAlchemyError as e:
    #                         transaction.rollback()
    #                         logger.error(f"Error occurred during deletion: {e}")
    #             except SQLAlchemyError as e:
    #                 logger.error(f"Connection error: {e}")



    def manual_import_data(self, table_name:str, df: pd.DataFrame, commit: bool) -> None:
        """
        Import data from a DataFrame into a specified database table.

        This method converts the DataFrame into a list of dictionaries, representing rows to be inserted into the database table.
        It performs the insertion using SQLAlchemy's insert operation.

        Args:
            table_name (str): The name of the table where data will be inserted as per sql format.
            df (pd.DataFrame): The DataFrame containing data to be inserted.
            commit (bool): If True, commit the transaction; otherwise, roll back.

        Returns:
            None
        """
        if df is not None and not df.empty:
            # Convert DataFrame to list of dictionaries
            data_to_insert = df.to_dict(orient='records')
            if not data_to_insert:
                logger.warning(f"No data to insert into {table_name}.")
                return

            # Get table metadata
            table = tables.get(table_name)
            if table is None:
                logger.error(f"Table {table_name} not found in metadata.")
                return

            # Prepare insert query
            insert_query = insert(table).values(data_to_insert)

            try:
                with self.db_engine.connect() as connection:
                    # Execute insert query
                    result = connection.execute(insert_query)
                    if commit:
                        connection.commit()
                        logger.info(f"Inserted {result.rowcount} rows into {table_name}.")
                    else:
                        connection.rollback()
                        logger.info(f"Transaction rolled back for importing data into {table_name}.")

            except SQLAlchemyError as e:
                logger.critical(f"Error inserting data into {table_name}: {e}")
                connection.rollback()
                logger.error(f"Rolling back changes in {table_name} due to import error.")
            except Exception as e:
                logger.critical(f"Unknown error occurred: {e}")
                connection.rollback()
                logger.error(f"Rolling back changes in {table_name} due to an unknown error.")
        else:
            logger.warning(f"Empty DataFrame, no rows inserted into {table_name}.")



    def get_exchange_rate_from_db(self, currency: str) -> float | int:
        # Query for the most recent rate for the specified currency
        rate = (self.Session.query(ExchangeRate.exchange_rate)
                              .filter(ExchangeRate.currency == currency)
                              .order_by(desc(ExchangeRate.date))
                              .first())
        
        return rate[0] if rate else 0

    # def delete_tally_material_centre_and_datewise(self, table_name: str, 
    #                                             start_date: str, end_date: str, 
    #                                             material_centre:list, commit: bool):
    #     table_class = tables.get(table_name)
    #     if not table_class:
    #         logger.error(f"Table '{table_name}' not found in table mapping. Delete query failed to execute.")
    #         return

    #     if start_date > end_date:
    #         logger.error(f"Start date '{start_date}' should be less than or equal to end date '{end_date}'.")
    #         return

    #     date_condition = table_class.date.between(start_date, end_date)
    #     material_centre_condition = table_class.material_centre.in_(material_centre)
    #     delete_query = delete(table_class).where(and_(date_condition, material_centre_condition))
        
    #     try:
    #         with self.db_engine.connect() as connection:
    #             transaction = connection.begin()
    #             try:
    #                 result = connection.execute(delete_query)
    #                 deleted_count = result.rowcount
    #                 logger.info(f"Deleted {deleted_count} rows from '{table_name}' between {start_date} and {end_date}.")
                    
    #                 if commit:
    #                     transaction.commit()
    #                     logger.info("Transaction committed.")
    #                 else:
    #                     transaction.rollback()
    #                     logger.info("Transaction not committed.")
    #             except SQLAlchemyError as e:
    #                 transaction.rollback()
    #                 logger.error(f"Error occurred during deletion: {e}")
    #     except SQLAlchemyError as e:
    #         logger.error(f"Connection error: {e}")


    def delete_tally_material_centre_and_datewise(self, table_name: str, 
                                              start_date: str = None, end_date: str = None, 
                                              material_centre: list = None, commit: bool = True):
        table_class = tables.get(table_name)
        if not table_class:
            logger.error(f"Table '{table_name}' not found in table mapping. Delete query failed.")
            return

        from sqlalchemy.inspection import inspect
        from sqlalchemy.exc import SQLAlchemyError

        # Build dynamic WHERE conditions
        conditions = []

        # Add material centre condition if applicable
        if material_centre:
            conditions.append(table_class.material_centre.in_(material_centre))

        # Check if 'date' column exists before applying date filter
        table_columns = [col.key for col in inspect(table_class).columns]
        if 'date' in table_columns and start_date and end_date:
            if start_date > end_date:
                logger.error(f"Start date '{start_date}' should be <= end date '{end_date}'.")
                return
            conditions.append(table_class.date.between(start_date, end_date))
        elif start_date or end_date:
            logger.warning(f"Table '{table_name}' does not support date-based filtering. Skipping date condition.")

        if not conditions:
            logger.warning("No valid filter conditions provided. Aborting delete operation.")
            return

        # Construct the delete query
        delete_query = delete(table_class).where(and_(*conditions))

        try:
            with self.db_engine.connect() as connection:
                transaction = connection.begin()
                try:
                    result = connection.execute(delete_query)
                    deleted_count = result.rowcount or 0
                    logger.info(f"Deleted {deleted_count} rows from '{table_name}' for material centre(s): {material_centre} "
                                f"{f'between {start_date} and {end_date}' if start_date and end_date else ''}.")

                    if commit:
                        transaction.commit()
                        logger.info("Transaction committed.")
                    else:
                        transaction.rollback()
                        logger.info("Transaction not committed.")
                except SQLAlchemyError as e:
                    transaction.rollback()
                    logger.error(f"Error occurred during deletion: {e}")
        except SQLAlchemyError as e:
            logger.error(f"Connection error: {e}")
