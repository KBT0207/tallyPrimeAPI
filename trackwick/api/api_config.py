import pandas as pd
import requests
from dotenv import load_dotenv
import json
import os
from datetime import datetime
from typing import Optional, Dict, Any
from logging_config import logger



class APIError(Exception):
    """Custom exception for API-related errors"""
    pass


class TrackOlapAPI:
    """Main class for handling TrackOlap API interactions"""
    
    BASE_URL = "https://app.trackolap.com/cust/1/api"
    
    def __init__(self):
        logger.info("Initializing TrackOlapAPI")
        load_dotenv('.env')
        self.headers = {
            'Content-Type': 'application/json',
            'platform': 'API',
            'tlp-cid': os.getenv('CUST_ID'),
            'api-key': os.getenv('API_KEY'),
            'tlp-t': os.getenv('TLP_T')
        }
        self._cache = {}
        logger.debug(f"Headers initialized: {self.headers}")


    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """
        Make HTTP request to the API
        
        Args:
            method: HTTP method ('GET' or 'POST')
            endpoint: API endpoint
            data: Optional data for POST requests
        """
        url = f"{self.BASE_URL}/{endpoint}"
        logger.info(f"Making {method} request to {url}")
        if data:
            logger.debug(f"Request payload: {data}")

        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers)
            else:
                response = requests.post(url, headers=self.headers, data=json.dumps(data))
            
            response.raise_for_status()
            logger.info(f"Request to {url} successful")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request to {url} failed: {e}")
            raise APIError(f"API request failed: {str(e)}")


    def get_report(self, report_id: str, start_date: Optional[str] = None, 
                   end_date: Optional[str] = None) -> pd.DataFrame:
        """
        Fetch and process report data
        
        Args:
            report_id: Report identifier
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
        """
        today = datetime.today().date().strftime("%Y-%m-%d")
        start_date = start_date or today
        end_date = end_date or today

        logger.info(f"Fetching report with ID {report_id} from {start_date} to {end_date}")
        cache_key = (report_id, start_date, end_date)
        if cache_key in self._cache:
            logger.info(f"Cache hit for report {report_id}")
            return self._cache[cache_key]

        endpoint = f"report/get?report_id={report_id}&start_date={start_date}&end_date={end_date}"
        response = self._make_request('GET', endpoint)
        
        logger.info("Processing report data")
        df = self.process_data(response)
        self._cache[cache_key] = df
        return df


    def process_data(self, response: dict):
        """
        Processes the API response and returns a DataFrame.
        Args:
            api_response (dict): The API response dictionary.
        Returns:
            pd.DataFrame: Processed data in DataFrame format.
        """
        if not response:
            print("No data to process.")
            return None

        column_data = {}
        for col_name in response.get('columns', []):
            column_data[col_name] = []
            col_index = response['columns'].index(col_name)
            for row in response.get('rows', []):
                cell_value = row[col_index]['data'][0].get('value')
                column_data[col_name].append(cell_value)

        return pd.DataFrame(column_data)


    def get_customers(self, page_size: int = 5, page_number: int = 0) -> Dict[str, Any]:
        """
        Get list of customers with pagination
        """
        logger.info(f"Fetching customers with page size {page_size} and page number {page_number}")
        cache_key = ('customers', page_size, page_number)
        if cache_key in self._cache:
            logger.info("Cache hit for customer list")
            return self._cache[cache_key]

        endpoint = f"customer/list?pt={page_size}&pn={page_number}"
        response = self._make_request('GET', endpoint)
        self._cache[cache_key] = response
        return response


    def get_tasks(self, page_size: int = 5, page_number: int = 0, 
                  start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get list of tasks with pagination
        """
        today = datetime.today().date().strftime("%Y-%m-%d")
        start_date = start_date or today
        end_date = end_date or today

        logger.info(f"Fetching tasks from {start_date} to {end_date}, page size {page_size}, page number {page_number}")
        cache_key = ('tasks', page_size, page_number, start_date, end_date)
        if cache_key in self._cache:
            logger.info("Cache hit for task list")
            return self._cache[cache_key]

        endpoint = f"task/list?pt={page_size}&pn={page_number}&start_date={start_date}&end_date={end_date}"
        response = self._make_request('GET', endpoint)
        self._cache[cache_key] = response
        return response


    def get_employees(self, page_size: int = 20, page_number: int = 1, 
                      asset_ids: Optional[str] = None, search_query: Optional[str] = None) -> Dict[str, Any]:
        """
        Get list of employees with pagination and filters
        """
        params = [f"pt={page_size}", f"pn={page_number}"]
        if asset_ids:
            params.append(f"asset_ids={asset_ids}")
        if search_query:
            params.append(f"q={search_query}")

        logger.info(f"Fetching employees with filters: page size {page_size}, page number {page_number}, asset IDs {asset_ids}, search query {search_query}")
        cache_key = ('employees', page_size, page_number, asset_ids, search_query)
        if cache_key in self._cache:
            logger.info("Cache hit for employee list")
            return self._cache[cache_key]

        endpoint = f"asset/list?{'&'.join(params)}"
        response = self._make_request('GET', endpoint)
        self._cache[cache_key] = response
        return response


    def process_employees_response(self, response: dict) -> pd.DataFrame:
        """
        Processes the 'get_employees' API response and converts it to a DataFrame.
        """
        if not response.get('s') or 'data' not in response:
            logger.error("Invalid or empty response data")
            raise ValueError("Invalid or empty response data")

        logger.info("Transforming employee response into DataFrame")
        employees = []
        for emp in response['data']:
            employees.append({
                'ID': emp['id'],
                'Login': emp['login'],
                'Name': emp['name'],
                'Mobile': emp['mobile'],
                'Employee ID': emp['empId'],
                'Type': emp['type'],
                'Reporting Manager': emp['reportingManager']['name'] if 'reportingManager' in emp else None,
                'Functional Managers': ", ".join([fm['name'] for fm in emp.get('functionalManagers', [])])
            })

        return pd.DataFrame(employees)


    def update_customer(self, customer_id: str, update_data: Dict[str, Any]) -> Dict:
        """
        Update customer information
        
        Args:
            customer_id: Customer identifier
            update_data: Dictionary containing customer data to update
        """
        endpoint = f"customer/update?id={customer_id}"
        return self._make_request('POST', endpoint, update_data)


    def get_customer_by_id(self, customer_id: str) -> Dict:
        """
        Retrieve customer information
        
        Args:
            customer_id: Customer identifier
        """
        endpoint = f"customer/get?id={customer_id}"
        return self._make_request('GET', endpoint)






