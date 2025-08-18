from apis import get_rainfall_data, get_market_price
from datetime import date

# Example: Test Rainfall API
district = "Bahraich"
query_date = str(date.today())  # today's date
rainfall_data = get_rainfall_data(district, query_date)
print("Rainfall Data:", rainfall_data)

# Example: Test Market Price API
commodity = "Wheat"
market_data = get_market_price(commodity, query_date, district)
print("Market Price Data:", market_data)
