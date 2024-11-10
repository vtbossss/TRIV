import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

AGRO_API_KEY = os.getenv('API_KEY', 'default_api_key')
AGRO_API_URL = 'https://api.agromonitoring.com/agro/1.0/ndvi/history'

def fetch_agro_ndvi_data(polygon_id, start_date_str, end_date_str):
    """
    Fetch NDVI data from Agromonitoring API.
    Validates dates and handles API response errors.
    """
    # Validate and parse the start_date and end_date
    def validate_date(date_str):
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return None

    # Parse and validate the dates
    start_date = validate_date(start_date_str)
    end_date = validate_date(end_date_str)

    if not start_date or not end_date:
        return {"error": "Invalid date format. Please use 'YYYY-MM-DD'."}
    
    # Prepare parameters for the API request (Convert to Unix timestamps)
    params = {
        'polyid': polygon_id,
        'start': int(start_date.timestamp()),  # Unix timestamp for start date
        'end': int(end_date.timestamp()),      # Unix timestamp for end date
        'appid': AGRO_API_KEY
    }

    try:
        response = requests.get(AGRO_API_URL, params=params, timeout=100)
        
        # Check if the response was successful
        if response.status_code == 200:
            data = response.json()
            # Check if the response contains the expected data
            if data and isinstance(data, list):
                return data
            else:
                return {"error": "No data found for the given date range."}
        
        # Handle different API response errors
        else:
            return {"error": f"API request failed with status code {response.status_code}."}
    
    except requests.exceptions.RequestException as e:
        # Handle any network or request exceptions
        return {"error": f"An error occurred while fetching data: {str(e)}"}

polygon_id ='672b66d8287b0e7adefd1a54'
start_date = '2015-01-01'
end_date = '2024-08-19'


