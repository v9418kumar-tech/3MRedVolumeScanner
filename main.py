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

    signals = []

    print("5 Minute Red Green Volume Scanner Running", now)

    for symbol in stocks:

        try:
            data = yf.download(
                symbol,
                period="1d",
                interval="5m",
                progress=False
            )

            if len(data) < 2:
                continue

            current = data.iloc[-1]
            previous = data.iloc[-2]

            current_open = float(current["Open"].iloc[0])
            current_close = float(current["Close"].iloc[0])
            current_volume = float(current["Volume"].iloc[0])

            previous_open = float(previous["Open"].iloc[0])
            previous_close = float(previous["Close"].iloc[0])
            previous_volume = float(previous["Volume"].iloc[0])


            if (
                current_close < current_open
                and previous_close > previous_open
                and current_volume > previous_volume
            ):
                signals.append(symbol)


        except Exception as e:
            print(symbol, e)


    print("\n🚨 ALERT")

    if signals:
        for stock in signals:
            print(stock, "Condition Completed")
    else:
        print("No Signal Found")


scanner()
