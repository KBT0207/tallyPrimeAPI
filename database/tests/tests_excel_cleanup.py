from database.busy_data_processor import (
    get_filename, get_compname,
)
from database.busy_data_processor import ExcelProcessor


def test_get_filename():
    path_1 = "C:\\automated_scripts\\comp0005\\sales\\comp0005_sales_20-Apr-2024.xlsx"
    assert get_filename(path_1) == "sales"

    path_2 = "C:\\automated_scripts\\comp0005\\sales_return\\comp0005_sales_return_20-Apr-2024.xlsx"
    assert get_filename(path_2) == "sales_return"


def test_get_filename():
    path_1 = "C:\\automated_scripts\\comp0005\\sales\\comp0005_sales_20-Apr-2024.xlsx"
    assert get_compname(path_1) == "comp0005"


