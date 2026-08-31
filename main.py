import yfinance as yf
from datetime import datetime


def scanner():

    now = datetime.now().strftime("%H:%M:%S")

    with open("stocks.txt", "r") as file:
        stocks = [x.strip() for x in file.readlines() if x.strip()]

    alerts = []

    print("5 Min Red Green Volume Scanner Running", now)

    for symbol in stocks:

        try:
            data = yf.download(
                symbol,
                period="2d",
                interval="5m",
                progress=False
            )

            if len(data) < 3:
                continue

            # Last two completed candles
            previous = data.iloc[-2]
            current = data.iloc[-1]

            previous_open = float(previous["Open"])
            previous_close = float(previous["Close"])
            previous_volume = float(previous["Volume"])

            current_open = float(current["Open"])
            current_close = float(current["Close"])
            current_volume = float(current["Volume"])


            # Condition
            if (
                previous_close > previous_open
                and current_close < current_open
                and current_volume > previous_volume
            ):

                alerts.append(
                    f"""
🚨 5 Min Red Volume Alert

Stock: {symbol}

Previous Green Volume:
{int(previous_volume)}

Current Red Volume:
{int(current_volume)}

Condition Completed ✅
"""
                )


        except Exception as e:
            print(symbol, e)


    if alerts:
        print("\n".join(alerts))

    else:
        print("No Signal Found")


scanner()
