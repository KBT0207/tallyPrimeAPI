import pandas as  pd
from Database.db_crud import DatabaseCrud  # Assuming you have this module
from Reports import (
    sales_price_validation
)



class Reports(DatabaseCrud):
    def __init__(self):
        self.sales_reports = sales_price_validation.SalesPriceValidation

    def sales_price_validation(self, from_date: str, to_date: str, exceptions: list = None) -> pd.DataFrame:
        return self.sales_price_validation(from_date, to_date, exceptions)
    


