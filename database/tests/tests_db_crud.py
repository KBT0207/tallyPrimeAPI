import pytest
from sqlalchemy import create_engine, Column, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date
from database.db_crud import DatabaseCrud

# Define a SQLAlchemy base for creating test tables
Base = declarative_base()

# Define a test table for use in the tests
class TestTable(Base):
    __tablename__ = 'test_table'
    id = Column('id', primary_key=True)
    date = Column('date', Date)

# Create an in-memory SQLite database engine for testing
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)

# Create a sessionmaker bound to the test engine
Session = sessionmaker(bind=engine)

# Fixture to set up a test database CRUD instance
@pytest.fixture
def test_db_crud():
    db_connector = DatabaseCrud(db_connector=engine)
    return db_connector

# Test case for delete_date_range_query method
def test_delete_date_range_query(test_db_crud):
    # Create a session for the test database CRUD instance
    session = Session()

    # Insert test data into the test table
    session.add_all([
        TestTable(date=date(2024, 1, 1)),
        TestTable(date=date(2024, 2, 1)),
        TestTable(date=date(2024, 3, 1)),
    ])
    session.commit()

    # Perform the delete operation using the delete_date_range_query method
    test_db_crud.delete_date_range_query('test_table', date(2024, 2, 1), date(2024, 3, 1))

    # Check that the rows were deleted
    assert session.query(TestTable).count() == 2

    # Close the session
    session.close()
