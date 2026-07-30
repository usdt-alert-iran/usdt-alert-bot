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

    if price is None:
        return

    now = datetime.now()

    print(
        datetime.now(),
        "USDT:",
        price
    )

    if price >= TARGET_PRICE:
      if start_time is None:
            start_time = now
            send_message(
                f"🟢 تتر وارد محدوده شد\n"
                f"قیمت فعلی: {price:,.0f} تومان\n"
                f"زمان شروع بررسی: {now}"
            )
        elif now - start_time >= timedelta(hours=4) and not alert_sent:

            send_message(
                f"🚀 شرط ۴ ساعت تایید شد\n\n"
                f"تتر حداقل ۴ ساعت بالای {TARGET_PRICE:,} تومان ماند.\n"
                f"قیمت فعلی: {price:,.0f} تومان\n\n"
                f"تارگت‌های احتمالی:\n"
                f"🎯 200,000\n"
                f"🎯 205,000"
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
