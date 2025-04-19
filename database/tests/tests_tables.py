import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models.busy_models.busy_reports import SalesKBBIO
from database.models.base import Base

# Create an in-memory SQLite engine for testing
engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
session = Session()

@pytest.fixture(scope='module')
def setup_database():
    # Create all tables defined in the declarative base
    Base.metadata.create_all(engine)
    yield  # Run tests
    # Drop all tables after tests are completed
    Base.metadata.drop_all(engine)

def test_sales_kbbio_table(setup_database):
    # Create a new SalesKBBIO instance
    sales_kbbio = SalesKBBIO(name='John Doe', address='123 Main St', email='johndoe@example.com')

    # Add the instance to the session
    session.add(sales_kbbio)
    session.commit()

    # Retrieve the instance from the database
    result = session.query(SalesKBBIO).filter_by(name='John Doe').first()

    # Assert that the instance was successfully added and retrieved
    assert result is not None
    assert result.name == 'John Doe'
    assert result.address == '123 Main St'
    assert result.email == 'johndoe@example.com'
