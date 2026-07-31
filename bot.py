import os
import time
import requests
from datetime import datetime, timedelta
from telegram import Bot

# تنظیمات
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

bot = Bot(token=TOKEN)

TARGET_PRICE = 194000
CHECK_INTERVAL = 60  # هر 1 دقیقه بررسی شود

start_time = None
alert_sent = False


def get_usdt_price():
    try:
        url = "https://api.nobitex.ir/market/stats"
        params = {
            "symbol": "USDTIRT"
        }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        price = float(data["stats"]["usdtirt"]["latest"])
        return price

    except Exception as e:
        print("Error price:", e)
        return None


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

    if price >= TARGET_PRICE:
        if start_time is None:
            start_time = now
            send_message(f"USDT reached {price}. Checking 4 hours...")
        
    elif now - start_time >= timedelta(hours=4) and not alert_sent:
            send_message(f"4 hours confirmed. Current price: {price}")
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
