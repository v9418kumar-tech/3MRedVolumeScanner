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

    print("5 Min Red Green Volume Scanner Running")
    print("Time:", now)


    for symbol in stocks:

        try:

            data = yf.download(
                symbol,
                period="2d",
                interval="5m",
                progress=False
            )

            if data.empty or len(data) < 3:
                continue


            current = data.iloc[-1]
            previous = data.iloc[-2]


            current_open = float(current["Open"])
            current_close = float(current["Close"])

            previous_open = float(previous["Open"])
            previous_close = float(previous["Close"])


            current_volume = int(current["Volume"])
            previous_volume = int(previous["Volume"])


            # Current candle Red
            red_candle = current_close < current_open


            # Previous candle Green
            green_previous = previous_close > previous_open


            # Current volume greater than previous volume
            volume_condition = current_volume > previous_volume


            if red_candle and green_previous and volume_condition:

                result.append(
                    f"🚨 ALERT {symbol} | Current Volume: {current_volume} | Previous Volume: {previous_volume}"
                )


        except Exception as e:
            print(symbol, "Error")


    print("\n🚨 5 Min Red Green Volume Scanner")

    if result:

        for r in result:
            print(r)

    else:
        print("No Signal Found")


scanner()
