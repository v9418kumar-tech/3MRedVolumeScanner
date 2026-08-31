import yfinance as yf
import pandas as pd
from datetime import datetime

def scanner():

    now = datetime.now().strftime("%H:%M:%S")

    stocks = [
        "RELIANCE.NS",
        "TATAMOTORS.NS",
        "HDFCBANK.NS",
        "ICICIBANK.NS",
        "SBIN.NS"
    ]

    result = []

    print("5 Minute Volume Scanner Running", now)

    for symbol in stocks:

        try:
            data = yf.download(
                symbol,
                period="1d",
                interval="5m",
                progress=False
            )

            if len(data) < 5:
                continue

            data["Volume_Avg"] = data["Volume"].rolling(5).mean()

            last = data.iloc[-1]

            volume = float(last["Volume"])
            avg_volume = float(last["Volume_Avg"])

            if volume > avg_volume * 3:
                result.append(
                    f"{symbol} Volume Spike {volume:.0f}"
                )

        except Exception as e:
            print(symbol, e)

    message = f"""
🚨 5 Min Volume Scanner

Time: {now}

"""

    if result:
        message += "\n".join(result)
    else:
        message += "No Volume Spike Found"

    print(message)


scanner()
