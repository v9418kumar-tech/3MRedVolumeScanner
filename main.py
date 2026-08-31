import requests
import time
from datetime import datetime

# Telegram details (बाद में भरेंगे)
BOT_TOKEN = ""
CHAT_ID = ""

def send_message(msg):
    if BOT_TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def scanner():
    now = datetime.now().strftime("%H:%M:%S")

    print("5 Minute Volume Scanner Running", now)

    # yahan market data API jodenge
    # abhi testing message

    message = f"""
🚨 5 Min Volume Scanner
Time: {now}

Scanner Active ✅
Waiting for breakout stocks...
"""

    print(message)
    send_message(message)


while True:
    scanner()
    time.sleep(300)
