# main.py
from flask import Flask, request
import requests
import google.generativeai as genai
from datetime import date
from apis import get_rainfall_data, get_market_price

app = Flask(__name__)

# Telegram setup
TELEGRAM_TOKEN = "8287552481:AAEqRTN5KRtqsy4_M3EZ4CKibIb_-y9pVY0"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# Gemini setup
genai.configure(api_key="AIzaSyCbAUR4Cobc8MVlKaStSOLJSYsbofvhpOE")
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Extraction Functions ---
def extract_district(text):
    # TODO: Improve with NLP if needed
    # Placeholder: returns first word capitalized as district
    words = text.split()
    return words[0].capitalize() if words else "UnknownDistrict"

def extract_date(text):
    # Default to today
    return str(date.today())

def extract_commodity(text):
    # Placeholder: returns first word capitalized as commodity
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

        # Detect if query is about rainfall
        if "rainfall" in user_text:
            district = extract_district(user_text)
            query_date = extract_date(user_text)
            api_data = get_rainfall_data(district, query_date)
            if not api_data:
                api_data = "Sorry, rainfall data is temporarily unavailable."
            user_text = f"{user_text}\n\nOfficial Data: {api_data}"

        # Detect if query is about market price
        elif "market price" in user_text or "price of" in user_text:
            commodity = extract_commodity(user_text)
            query_date = extract_date(user_text)
            district = extract_district(user_text)  # optional
            api_data = get_market_price(commodity, query_date, district)
            if not api_data:
                api_data = "Sorry, market price data is temporarily unavailable."
            user_text = f"{user_text}\n\nOfficial Data: {api_data}"

        # Generate response from Gemini
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




