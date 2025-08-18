# apis.py
import requests

# Replace with your actual API URLs and token
RAIN_API_TOKEN = "579b464db66ec23bdd000001ce8cce7242164a315a8d3069bbb48a27"
MARKET_API_TOKEN = "579b464db66ec23bdd000001ce8cce7242164a315a8d3069bbb48a27"

def get_rainfall_data(district, date):
    url = f"https://data.gov.in/api/rainfall?district={district}&date={date}"
    headers = {"Authorization": f"Token {RAIN_API_TOKEN}"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Format response (adjust keys based on API response)
        return f"Rainfall in {district} on {date}: {data.get('rainfall_mm', 'Data not found')} mm"
    except Exception as e:
        return f"Could not fetch rainfall data: {e}"

def get_market_price(commodity, date, district=None):
    url = f"https://data.gov.in/api/market-price?commodity={commodity}&date={date}"
    if district:
        url += f"&district={district}"
    headers = {"Authorization": f"Token {MARKET_API_TOKEN}"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return f"Market price of {commodity} on {date}: {data.get('price', 'Data not found')} INR"
    except Exception as e:
        return f"Could not fetch market price: {e}"
