python
import requests
import schedule
import time
from telegram import Bot

BOT_TOKEN = "8016783825:AAEA3W83-Ig9SED9uJHtmt10RFVWdMXeHeQ"
CHANNEL_ID = "@VeeWoStore"

bot = Bot(token=BOT_TOKEN)

-----------------------------

دریافت قیمت‌ها

-----------------------------
def get_prices():
    # قیمت دلار به تومان از نوبیتکس
    try:
        r = requests.get("https://api.nobitex.ir/v2/orderbook/USDTIRT").json()
        usdt_toman = int(r["lastTradePrice"])
    except:
        usdt_toman = None

    # لیست ارزها
    symbols = [
        "BTCUSDT", "ETHUSDT", "SOLUSDT", "TONUSDT",
        "SUIUSDT", "BNBUSDT", "TRXUSDT", "XRPUSDT"
    ]

    crypto_prices = {}

    for sym in symbols:
        try:
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={sym}"
            data = requests.get(url).json()
            crypto_prices[sym.replace("USDT", "")] = float(data["price"])
        except:
            crypto_prices[sym.replace("USDT", "")] = None

    return usdttoman, cryptoprices


-----------------------------

ساخت پیام خوش‌فرم

-----------------------------
def build_message():
    usdttoman, crypto = getprices()

    msg = "📊 آپدیت روزانه قیمت‌ها\n\n"

    if usdt_toman:
        msg += f"💵 دلار: {usdt_toman:,} تومان\n\n"

    msg += "💠 ارزهای دیجیتال (دلاری):\n"
    for k, v in crypto.items():
        if v:
            msg += f"• {k}: {v:.2f} $\n"
        else:
            msg += f"• {k}: ❌\n"

    msg += "\n⏱️ آپدیت خودکار هر ۲۴ ساعت"

    return msg


-----------------------------

ارسال پیام در کانال

-----------------------------
def send_update():
    message = build_message()
    bot.sendmessage(chatid=CHANNELID, text=message, parsemode="Markdown")


-----------------------------

زمان‌بندی ۲۴ ساعته

-----------------------------
schedule.every(24).hours.do(send_update)

print("Bot is running...")

send_update()  # اولین پیام بلافاصله ارسال شود

while True:
    schedule.run_pending()
    time.sleep(1)

