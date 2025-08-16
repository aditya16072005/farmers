from flask import Flask, request
import requests
import google.generativeai as genai

app = Flask(__name__)

# Telegram bot token
TELEGRAM_TOKEN = "your_token_here"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# Gemini setup
genai.configure(api_key="your_gemini_api_key")
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/')
def home():
    return "Bot is running on Render!"

@app.route('/telegram/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"]["text"]

        # Get Gemini reply
        response = model.generate_content(user_text)
        bot_reply = response.text

        # Send back to Telegram
        send_message(chat_id, bot_reply)

    return "ok"

def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)
