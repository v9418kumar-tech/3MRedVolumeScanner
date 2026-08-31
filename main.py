import yfinance as yf
from datetime import datetime


def scanner():

    now = datetime.now().strftime("%H:%M:%S")

    # Read stocks from stocks.txt
    with open("stocks.txt", "r") as file:
        stocks = [line.strip() for line in file if line.strip()]

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

            current_open = float(current["Open"])
            current_close = float(current["Close"])
            current_volume = float(current["Volume"])

            previous_open = float(previous["Open"])
            previous_close = float(previous["Close"])
            previous_volume = float(previous["Volume"])


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
