import requests
import schedule
import time
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

BOT_TOKEN = "8016783825:AAEA3W83-Ig9SED9uJHtmt10RFVWdMXeHeQ"
CHANNEL_ID = "@VeeWoStore"

bot = Bot(token=BOT_TOKEN)

# -----------------------------
# دریافت قیمت‌ها
# -----------------------------
def get_prices():
    # تلاش برای دریافت قیمت تتر با پروکسی
    try:
        url = "https://api.allorigins.win/raw?url=https://api.exir.io/v1/ticker/usdt-irt"
        r = requests.get(url, timeout=10).json()
        usdt_toman = int(r["last"])
    except:
        usdt_toman = None

    # قیمت انس جهانی طلا (XAU/USD)
    try:
        gold = requests.get(
            "https://api.binance.com/api/v3/ticker/price?symbol=XAUUSD",
            timeout=10
        ).json()
        gold_price = float(gold["price"])
    except:
        gold_price = None

    # قیمت ارزهای دیجیتال از بایننس
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

    return usdt_toman, gold_price, crypto_prices

# -----------------------------
# ساخت پیام
# -----------------------------
def build_message():
    usdt_toman, gold_price, crypto = get_prices()

    msg = "📊 آپدیت روزانه قیمت‌ها\n\n"

    # قیمت تتر
    if usdt_toman:
        msg += f"💵 تتر (USDT): {usdt_toman:,} تومان\n\n"
    else:
        msg += "💵 تتر (USDT): ❌ (دریافت نشد)\n\n"

    # انس جهانی طلا
    if gold_price:
        msg += f"🥇 انس جهانی طلا: {gold_price:.2f} دلار\n\n"
    else:
        msg += "🥇 انس جهانی طلا: ❌\n\n"

    # قیمت ارزها
    msg += "💠 ارزهای دیجیتال (دلاری):\n"
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
