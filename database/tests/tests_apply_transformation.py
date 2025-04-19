from database.busy_data_processor import (
    apply_sales_transformation,
    apply_sales_return_transformation, apply_sales_order_transformation,
    apply_material_received_from_party_transformation, apply_material_issued_to_party_transformation
)
import pytest
import pandas as pd
from pandas.testing import assert_frame_equal

# Define paths to sample files
valid_file_path = "path/to/valid_file.xlsx"
empty_file_path = "path/to/empty_file.xlsx"
nonexistent_file_path = "path/to/nonexistent_file.xlsx"

def test_apply_sales_transformation_valid_file():
    # Test valid file path and top_row value
    transformed_df = apply_sales_transformation(valid_file_path, 1)
    assert isinstance(transformed_df, pd.DataFrame)
    # Add more assertions to validate specific transformations if needed

def test_apply_sales_transformation_empty_file():
    # Test empty file scenario
    transformed_df = apply_sales_transformation(empty_file_path, 1)
    assert transformed_df is None

def test_apply_sales_transformation_file_not_found(caplog):
    # Test FileNotFoundError scenario
    transformed_df = apply_sales_transformation(nonexistent_file_path, 1)
    assert transformed_df is None
    assert "Excel File not found" in caplog.text

# Add more test cases as needed to cover different scenarios



