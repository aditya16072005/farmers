from flask import Flask, request
import requests
import google.generativeai as genai
from apis import get_rainfall_data, get_market_price

app = Flask(__name__)

# Telegram bot token
TELEGRAM_TOKEN = "8287552481:AAEqRTN5KRtqsy4_M3EZ4CKibIb_-y9pVY0"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# Gemini setup
genai.configure(api_key="AIzaSyCbAUR4Cobc8MVlKaStSOLJSYsbofvhpOE")
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/')
def home():
    return "Bot is running on Render!"

@app.route('/telegram/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"]["text"].lower()

        # --- Step 3: Detect if query matches an API ---
        if "rainfall" in user_text:
            district = extract_district(user_text)
            date = extract_date(user_text)
            api_data = get_rainfall_data(district, date)
            user_text = f"{user_text}\n\nOfficial Data: {api_data}"

        elif "market price" in user_text or "price of" in user_text:
            commodity = extract_commodity(user_text)
            date = extract_date(user_text)
            district = extract_district(user_text)  # optional
            api_data = get_market_price(commodity, date, district)
            user_text = f"{user_text}\n\nOfficial Data: {api_data}"

        # --- Send user_text (with API data included) to Gemini ---
        response = model.generate_content(user_text)
        bot_reply = response.output_text
        send_message(chat_id, bot_reply)

    return "ok"


def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)



