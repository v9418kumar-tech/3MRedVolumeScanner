import yfinance as yf
from datetime import datetime

def scanner():

    now = datetime.now().strftime("%H:%M:%S")

    stocks = []

    try:
        with open("stocks.txt", "r") as f:
            stocks = [x.strip() for x in f.readlines() if x.strip()]
    except:
        print("stocks.txt not found")
        return

    result = []

    print("5 Min Red Green Volume Scanner Running", now)

    for symbol in stocks:

        try:

            data = yf.download(
                symbol,
                period="2d",
                interval="5m",
                progress=False
            )

            if data.empty or len(data) < 2:
                continue


            current = data.iloc[-1]
            previous = data.iloc[-2]


            current_open = float(current["Open"].iloc[0])
            current_close = float(current["Close"].iloc[0])

            previous_open = float(previous["Open"].iloc[0])
            previous_close = float(previous["Close"].iloc[0])


            current_volume = int(current["Volume"].iloc[0])
            previous_volume = int(previous["Volume"].iloc[0])


            # Current candle Red
            red_candle = current_close < current_open


            # Previous candle Green
            green_previous = previous_close > previous_open


            # Current volume greater than previous volume
            volume_condition = current_volume > previous_volume


            if red_candle and green_previous and volume_condition:

                result.append(
                    f"{symbol} ALERT | Current Volume: {current_volume} | Previous Volume: {previous_volume}"
                )


        except Exception as e:
            print(symbol, e)


    print("\n🚨 5 Min Red Green Volume Scanner")

    print("Time:", now)


    if result:
        for r in result:
            print(r)
    else:
        print("No Signal Found")


scanner()
