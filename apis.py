import requests

# Rainfall API
def get_rainfall_data(district, date):
    url = f"https://data.gov.in/api/rainfall?district={district}&date={date}"
    headers = {"Authorization": "Token 579b464db66ec23bdd000001ce8cce7242164a315a8d3069bbb48a27"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # format data as readable string
        return f"Rainfall in {district} on {date}: {data['rainfall_mm']} mm"
    else:
        return "Could not fetch rainfall data."

# Market Prices API
def get_market_price(commodity, date, district=None):
    url = f"https://data.gov.in/api/market-price?commodity={commodity}&date={date}"
    if district:
        url += f"&district={district}"
    headers = {"Authorization": "Token 579b464db66ec23bdd000001ce8cce7242164a315a8d3069bbb48a27"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # format data as readable string
        return f"Market price of {commodity} on {date}: {data['price']} INR"
    else:
        return "Could not fetch market price."
