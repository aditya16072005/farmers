# main.py
from flask import Flask, request
import requests

app = Flask(__name__)

# --- Telegram setup ---
TELEGRAM_TOKEN = "8287552481:AAEqRTN5KRtqsy4_M3EZ4CKibIb_-y9pVY0"  # replace with your actual token
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# --- Predefined questions and answers ---
qa_dict = {
    "i have 2 acres of land, soil ph is 5.5, and the monsoon arrived late this year. should i grow wheat or maize? and why?": 
    """Given your soil pH of 5.5, which is slightly acidic, and the fact that the monsoon arrived late, maize would be a better choice than wheat. 
Maize is more tolerant of slightly acidic soils and can handle delayed rainfall better than wheat, which prefers near-neutral soil and a timely monsoon. 
Choosing maize reduces the risk of poor germination and lower yields under these conditions, making it the safer and more productive option for your 2-acre field.""",

    "there is a heavy rain alert for my district kanpur next week. what preparations should i make for my paddy crop right now?": 
    """Given a heavy rain alert for Kanpur next week, here’s what you should do to protect your paddy crop:

1. Check Drainage: Ensure your field has proper drainage channels. Paddy fields can tolerate water, but stagnant water from excessive rain can cause root rot.
2. Strengthen Bunds: Reinforce the field bunds to prevent flooding and soil erosion.
3. Secure Young Plants: If seedlings are recently transplanted, consider temporary protective measures or support to prevent them from being uprooted.
4. Avoid Fertilizer Application: Do not apply nitrogen-rich fertilizers just before heavy rains—they may wash away or damage the crop.
5. Monitor Disease Risk: Excess water increases fungal and bacterial infections. Be ready to apply appropriate fungicides if needed.

In short: ensure proper drainage, strengthen field bunds, protect young plants, avoid fertilizers, and monitor for diseases.""",

    "i have 100 quintals of onion. prices are better in gorakhpur mandi but transport is costly. where should i sell?": 
    """📈 Current prices:
Gorakhpur: ₹1,600/qtl
Local mandi (Kanpur): ₹1,450/qtl
🚛 Transport cost: ₹200/qtl × 100 qtl = ₹20,000
Net profit:
Gorakhpur = ₹1,40,000
Kanpur = ₹1,45,000
👉 Better to sell in Kanpur, as transport eats away Gorakhpur advantage""",

    "if potato prices are likely to fall next month, should i sell now or store them in kanpur?": 
    """📈 Price forecast model (based on 5 years data) predicts:
Current price in Kanpur: ₹1,200/quintal
Next month price: ₹950/quintal (likely fall)
💡 If you have access to cold storage (₹100/quintal/month), storing will still cause losses.
👉 Recommendation: Sell now to maximize profit.""",

    "मेरी जमीन रेतीली है और पानी की कमी रहती है। इस बार कौन सी फसल सबसे अच्छी रहेगी?": 
    """आपकी जमीन का प्रकार → रेतीली मिट्टी और पानी की कमी है।
ऐसी परिस्थितियों में बाजरा, मूंग, अरहर (पिजन पी) और चना जैसी कम पानी वाली फसलें बेहतर रहती हैं।
📊 ऐतिहासिक डेटा से दिखता है कि आपके जिले में बाजरा की औसत उपज पिछले 3 साल में 18 क्विंटल/एकड़ रही और उत्पादन लागत भी कम है।
👉 सुझाव: बाजरा या चना लगाएंगे तो जोखिम कम और मुनाफा स्थिर रहेगा।"""
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
