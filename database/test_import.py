import pandas as pd
from sqlalchemy import create_engine, insert
from database.sql_connector import db_engine
from utils.common_utils import tables



def test_importing(table_name, df: pd.DataFrame, commit=False):
    table = tables.get(table_name)
    with db_engine.connect() as connection:
        try:
            data_to_insert = df.to_dict(orient='records')
            if not data_to_insert:
                print(f"No data to insert into {table_name}.")
                return
            if table is None:
                print(f"Table {table_name} not found in metadata.")
                return

            insert_query = insert(table).values(data_to_insert)
            connection.execute(insert_query)
            if commit:
                connection.commit()  # commit the transaction
                print("Transaction committed successfully.")
            else:
                connection.rollback()
                print("Rollback successful.")
        except Exception as e:
            print(f"Error occurred during transaction: {e}")
