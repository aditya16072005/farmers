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
        # Safely extract rainfall value; adjust key based on API
        rainfall_mm = data.get("rainfall_mm")
        if rainfall_mm is None:
            return f"Rainfall data not available for {district} on {date}."
        return f"Rainfall in {district} on {date}: {rainfall_mm} mm"
    except requests.RequestException as e:
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
        price = data.get("price")
        if price is None:
            return f"Market price not available for {commodity} on {date}."
        return f"Market price of {commodity} on {date}: {price} INR"
    except requests.RequestException as e:
        return f"Could not fetch market price: {e}"
