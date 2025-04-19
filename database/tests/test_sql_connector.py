import pytest
import os
from database.sql_connector import DatabaseConnector

# Sample environment variables for testing
os.environ['DB_USERNAME'] = 'test_user'
os.environ['DB_PASSWORD'] = 'test_password'
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_PORT'] = '3306'
os.environ['DATABASE'] = 'test_db'


@pytest.fixture
def db_connector():
    # Initialize DatabaseConnector with test environment variables
    return DatabaseConnector(
        os.getenv('DB_USERNAME'),
        os.getenv('DB_PASSWORD'),
        os.getenv('DB_HOST'),
        os.getenv('DB_PORT'),
        os.getenv('DATABASE')
    )


def test_db_connector_instance(db_connector):
    assert isinstance(db_connector, DatabaseConnector)


def test_db_connector_attributes(db_connector):
    assert db_connector.username == 'test_user'
    assert db_connector.password == 'test_password'
    assert db_connector.host == 'localhost'
    assert db_connector.port == '3306'
    assert db_connector.database == 'test_db'


def test_db_engine(db_connector):
    # Check if the engine exists
    assert db_connector.engine is not None

    # Get the SQLAlchemy URL object from the engine
    url = db_connector.engine.url

    # Check individual components of the URL
    assert url.drivername == 'mysql+pymysql'
    assert url.username == 'test_user'
    assert url.password == 'test_password'  # Confirm password if needed
    assert url.host == 'localhost'
    assert url.port == 3306
    assert url.database == 'test_db'



