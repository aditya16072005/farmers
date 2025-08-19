# main.py
from flask import Flask, request
import requests
import google.generativeai as genai
from datetime import date
from apis import get_rainfall_data, get_market_price
import pandas as pd

app = Flask(__name__)

# Load crop prices from Excel
crop_prices_df = pd.read_excel("crop_prices.xlsx")  # replace with your file path
crop_prices = crop_prices_df.set_index("Crop")["Seed_Price"].to_dict()

# Telegram setup
TELEGRAM_TOKEN = "8287552481:AAEqRTN5KRtqsy4_M3EZ4CKibIb_-y9pVY0"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# Gemini setup
genai.configure(api_key="AIzaSyCbAUR4Cobc8MVlKaStSOLJSYsbofvhpOE")
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Extraction Functions ---
def extract_district(text):
    words = text.split()
    return words[0].capitalize() if words else "UnknownDistrict"

def extract_date(text):
    return str(date.today())

def extract_commodity(text):
    words = text.split()
    return words[0].capitalize() if words else "Wheat"

# --- Telegram webhook ---
@app.route('/telegram/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"]["text"].lower()
        api_data = ""
        bot_reply = None  # initialize

        # Detect if query is about rainfall
        if "rainfall" in user_text:
            district = extract_district(user_text)
            query_date = extract_date(user_text)
            api_data = get_rainfall_data(district, query_date)
            if not api_data:
                api_data = "Sorry, rainfall data is temporarily unavailable."
            bot_reply = f"Rainfall in {district} on {query_date}: {api_data}"

        # Detect if query is about seed price
        elif "seed price" in user_text or "price of seed" in user_text:
            found = False
            for crop in crop_prices:
                if crop.lower() in user_text:
                    bot_reply = f"Seed price of {crop} is {crop_prices[crop]} INR"
                    found = True
                    break
            if not found:
                bot_reply = "Sorry, seed price for this crop is not available."

        # Detect if query is about market price
        elif "market price" in user_text or "price of" in user_text:
            commodity = extract_commodity(user_text)
            query_date = extract_date(user_text)
            district = extract_district(user_text)  # optional
            api_data = get_market_price(commodity, query_date, district)
            if not api_data:
                api_data = "Sorry, market price data is temporarily unavailable."
            bot_reply = f"Market price of {commodity} on {query_date}: {api_data}"

        # If no specific data reply, use Gemini
        if not bot_reply:
            try:
                response = model.generate_content(user_text)
                bot_reply = getattr(response, "output_text", None)
                if not bot_reply:
                    bot_reply = getattr(response, "text", None)
                if not bot_reply:
                    bot_reply = "Sorry, could not generate reply."
            except Exception as e:
                bot_reply = f"Error generating response: {e}"

        # Send reply to Telegram
        send_message(chat_id, bot_reply)

    return "ok"

# --- Send message to Telegram ---
def send_message(chat_id, text):
    try:
        url = f"{TELEGRAM_API_URL}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Error sending message: {e}")

# --- Health check ---
@app.route('/')
def home():
    return "Bot is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
