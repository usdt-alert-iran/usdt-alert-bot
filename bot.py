import os
import time
import requests
from datetime import datetime, timedelta
from telegram import Bot

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

TARGET_PRICE = 194000
CHECK_INTERVAL = 60

bot = Bot(token=TOKEN)

start_time = None
alert_sent = False


def get_usdt_price():
    url = "https://api.nobitex.ir/v3/orderbook/USDTIRT"

    response = requests.get(url, timeout=10)
    data = response.json()

    price = float(data["lastTradePrice"])

    return price


def send_message(text):
    try:
        bot.send_message(
            chat_id=CHAT_ID,
            text=text
        )
    except Exception as e:
        print("Telegram error:", e)


def check_price():
    global start_time, alert_sent

    price = get_usdt_price()
    now = datetime.now()

    print("Current price:", price)

    if price >= TARGET_PRICE:

        if start_time is None:
            start_time = now

            send_message(
                f"🟢 USDT reached target\nPrice: {price}\n4 hour timer started."
            )

        elif now - start_time >= timedelta(hours=4) and not alert_sent:

            send_message(
                f"🚀 4 hours confirmed\nCurrent price: {price}"
            )

            alert_sent = True

    else:
        start_time = None
        alert_sent = False


while True:
    try:
        check_price()

    except Exception as e:
        print("Main error:", e)

    time.sleep(CHECK_INTERVAL)
