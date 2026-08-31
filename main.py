import yfinance as yf
from datetime import datetime


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


            current_open = float(current["Open"].item())
            current_close = float(current["Close"].item())

            previous_open = float(previous["Open"].item())
            previous_close = float(previous["Close"].item())


            current_volume = int(current["Volume"].item())
            previous_volume = int(previous["Volume"].item())


            # Current candle Red
            red = current_close < current_open


            # Previous candle Green
            green = previous_close > previous_open


            # Current volume greater than previous volume
            volume = current_volume > previous_volume


            if red and green and volume:

                print(
                    "🚨 ALERT",
                    symbol,
                    "| Current Volume:",
                    current_volume,
                    "| Previous Volume:",
                    previous_volume
                )


        except Exception:
            continue



scanner()
