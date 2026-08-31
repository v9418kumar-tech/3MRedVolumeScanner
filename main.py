import yfinance as yf
from datetime import datetime
import requests

TELEGRAM_TOKEN = "8908511972:AAFWn-0KKs6YkyFPyrhZpX7nKDUE87g9u8Y"
CHAT_ID = "7416362918"


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.get(
        url,
        params={
            "chat_id": CHAT_ID,
            "text": message
        }
    )


def scanner():

    print("5 Min Red Green Volume Scanner Running")
    print("Time:", datetime.now().strftime("%H:%M:%S"))

    try:
        with open("stocks.txt", "r") as f:
            stocks = [x.strip() for x in f if x.strip()]

    except:
        print("stocks.txt not found")
        return


    for symbol in stocks:

        try:
            data = yf.download(
                symbol,
                period="2d",
                interval="5m",
                progress=False,
                auto_adjust=False
            )

            if len(data) < 3:
                continue


            current = data.iloc[-2]
            previous = data.iloc[-3]


            current_open = float(current["Open"])
            current_close = float(current["Close"])

            previous_open = float(previous["Open"])
            previous_close = float(previous["Close"])


            current_volume = int(current["Volume"])
            previous_volume = int(previous["Volume"])


            red = current_close < current_open
            green = previous_close > previous_open
            volume = current_volume > previous_volume


            if red and green and volume:

                message = (
                    f"🚨 ALERT {symbol}\n"
                    f"Current Volume: {current_volume}\n"
                    f"Previous Volume: {previous_volume}"
                )

                print(message)

                send_telegram(message)


        except Exception:
            continue


scanner()
