import requests
import time
from datetime import datetime
import yfinance as yf
import pandas as pd

# Telegram details (baad me bharenge)
BOT_TOKEN = ""
CHAT_ID = ""


def send_message(msg):
    if BOT_TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": msg
        })


def scanner():

    now = datetime.now().strftime("%H:%M:%S")

    print("5 Minute Volume Scanner Running", now)

    symbol = "RELIANCE.NS"

    data = yf.download(
        symbol,
        period="1d",
        interval="5m"
    )

    print(data.tail())

    message = f"""
🚨 5 Min Volume Scanner

Time: {now}

Stock: {symbol}

Scanner Ready ✅
Yahoo Finance Data Connected
"""

    print(message)
    send_message(message)


scanner()
