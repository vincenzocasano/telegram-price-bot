import requests
import schedule
import time
from datetime import datetime
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

BOT_TOKEN = "8016783825:AAEA3W83-Ig9SED9uJHtmt10RFVWdMXeHeQ"
CHANNEL_ID = "@VeeWoStore"

bot = Bot(token=BOT_TOKEN)

# -----------------------------
# دریافت قیمت رمز ارزها
# -----------------------------
def get_crypto_prices():
    symbols = [
        "BTCUSDT", "ETHUSDT", "SOLUSDT", "TONUSDT",
        "SUIUSDT", "BNBUSDT", "TRXUSDT", "XRPUSDT"
    ]

    crypto_prices = {}

    for sym in symbols:
        try:
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={sym}"
            data = requests.get(url, timeout=10).json()
            crypto_prices[sym.replace("USDT", "")] = float(data["price"])
        except:
            crypto_prices[sym.replace("USDT", "")] = None

    return crypto_prices

# -----------------------------
# ساخت پیام
# -----------------------------
def build_message():
    crypto = get_crypto_prices()

    # تاریخ و ساعت
    now = datetime.now().strftime("%Y/%m/%d - %H:%M")

    msg = f"📊 آپدیت قیمت رمز‌ارزها\n"
    msg += f"📅 تاریخ: {now}\n\n"

    msg += "💠 قیمت‌ها (دلاری):\n"
    for k, v in crypto.items():
        if v:
            msg += f"• {k}: {v:.2f} $\n"
        else:
            msg += f"• {k}: ❌\n"

    msg += "\n⏱ آپدیت خودکار هر ۲۴ ساعت"

    return msg

# -----------------------------
# ارسال پیام + دکمه شیشه‌ای
# -----------------------------
def send_update():
    message = build_message()

    keyboard = [
        [InlineKeyboardButton("💰 خرید / فروش", url="https://t.me/VeeWoSup")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_message(
        chat_id=CHANNEL_ID,
        text=message,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# -----------------------------
# زمان‌بندی
# -----------------------------
schedule.every(24).hours.do(send_update)

print("Bot is running...")

send_update()

while True:
    schedule.run_pending()
    time.sleep(1)
