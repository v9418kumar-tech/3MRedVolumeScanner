import yfinance as yf
from datetime import datetime


def scanner():

    now = datetime.now().strftime("%H:%M:%S")

    stocks = [
        "RELIANCE.NS",
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

            if data.empty:
                continue

            data["Volume_Avg"] = data["Volume"].rolling(5).mean()

            last_volume = data["Volume"].iloc[-1]
avg_volume = data["Volume_Avg"].iloc[-1]

if hasattr(last_volume, "iloc"):
    last_volume = last_volume.iloc[0]

if hasattr(avg_volume, "iloc"):
    avg_volume = avg_volume.iloc[0]

last_volume = float(last_volume)
avg_volume = float(avg_volume)

            if last_volume > avg_volume * 3:

                result.append(
                    f"{symbol} Volume Spike {int(last_volume)}"
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
