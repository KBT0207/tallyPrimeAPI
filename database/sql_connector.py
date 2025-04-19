"""
Database Connector Module

This module provides a DatabaseConnector class for creating and 
managing database connections using SQLAlchemy.

Usage:
- Initialize an instance of DatabaseConnector with the 
required database connection parameters.
- Use the 'engine' attribute of the DatabaseConnector instance 
to access the SQLAlchemy engine for database operations.

Dependencies:
- sqlalchemy: Required for creating and managing database connections.
- dotenv: Used for loading environment variables from a .env file. 
"""

import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus



load_dotenv('.env')


class DatabaseConnector:
    """
    Database Connector Class

    Creates and manages database connections using SQLAlchemy.

    Attributes:
    - username (str): Database username.
    - password (str): Database password.
    - host (str): Database host address.
    - port (str): Database port number.
    - database (str): Database name.
    - engine (sqlalchemy.engine.base.Engine): SQLAlchemy engine for database operations.

    Methods:
    - get_db_string(): Returns the database connection string.
    """

    def __init__(self, username, password, host, port, database) -> None:
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.engine = create_engine(self.get_db_string(),isolation_level='READ COMMITTED')


    def get_db_string(self):
        """
        Return the database connection string.

        Returns:
        - str: Database connection string in the format 
        'mysql+pymysql://username:password@host:port/database?autocommit=false'.
        """
        encoded_username = quote_plus(self.username) 
        encoded_password = quote_plus(self.password) 
        return f'mysql+pymysql://{encoded_username}:{encoded_password}@{self.host}:{self.port}/{self.database}?autocommit=false'


USERNAME = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASSWORD')
HOST = os.getenv('DB_HOST')
PORT = os.getenv('DB_PORT')
KBBIO_DATABASE = os.getenv('KBBIO_DATABASE')

KBE_DATABASE = os.getenv('KBE_DATABASE')


kbbio_connector = DatabaseConnector(USERNAME, PASSWORD, HOST, PORT, KBBIO_DATABASE)
kbbio_engine = kbbio_connector.engine
kbbio_connection = kbbio_engine.connect()



kbe_connector = DatabaseConnector(USERNAME, PASSWORD, HOST, PORT, KBE_DATABASE)
kbe_engine = kbe_connector.engine
kbe_connection = kbe_engine.connect()


