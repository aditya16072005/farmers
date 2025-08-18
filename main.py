# main.py
from flask import Flask, request
import requests

app = Flask(__name__)

# --- Telegram setup ---
TELEGRAM_TOKEN = "8287552481:AAEqRTN5KRtqsy4_M3EZ4CKibIb_-y9pVY0"  # replace with your actual token
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# --- Predefined questions and answers ---
qa_dict = {
    "what is your name?": "I am FarmBot.",
    "what is the rainfall today?": "Rainfall today is 12mm.",
    "price of wheat seed": "The price of wheat seed is 500 INR per kg.",
    "best crop to sow": "Maize is the best crop to sow this season.",
    "how to contact support?": "You can contact support at support@farmers.com."
}

# --- Telegram webhook ---
@app.route('/telegram/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"]["text"].lower().strip()  # normalize input

        # Look up answer
        answer = qa_dict.get(user_text, "Sorry, I can only answer 5 specific questions.")

        # Send reply
        send_message(chat_id, answer)

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
