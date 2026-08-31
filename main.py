import yfinance as yf
from datetime import datetime
import smtplib
from email.message import EmailMessage


EMAIL_SENDER = "v58388761@gmail.com"
EMAIL_PASSWORD = "rctl hsla uaod qrut"
EMAIL_RECEIVER = "v58388761@gmail.com"


def send_email(message):
    msg = EmailMessage()
    msg["Subject"] = "Stock Scanner Alert"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg.set_content(message)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)


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

                send_email(message)


        except Exception:
            continue


scanner()
