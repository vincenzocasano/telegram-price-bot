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
    usdt_toman = None

    # قیمت تتر به تومان از نوبیتکس
    try:
        r = requests.get("https://api.nobitex.ir/v2/orderbook/USDTIRT", timeout=10)
        data = r.json()
        # لاگ ساختار دریافتی
        print("Nobitex response:", data)

        # حالت کلاسیک نوبیتکس: data["lastTradePrice"]
        if "lastTradePrice" in data:
            usdt_toman = int(float(data["lastTradePrice"]))
        # بعضی نسخه‌ها توی result هستند
        elif "result" in data and "lastTradePrice" in data["result"]:
            usdt_toman = int(float(data["result"]["lastTradePrice"]))
    except Exception as e:
        print("Error fetching USDTIRT from Nobitex:", e)
        usdt_toman = None

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
        except Exception as e:
            print(f"Error fetching {sym} from Binance:", e)
            crypto_prices[sym.replace("USDT", "")] = None

    return usdt_toman, crypto_prices

# -----------------------------
# ساخت پیام خوش‌فرم
# -----------------------------
def build_message():
    usdt_toman, crypto = get_prices()

    msg = "📊 آپدیت روزانه قیمت‌ها\n\n"

    # قیمت تتر
    if usdt_toman is not None:
        msg += f"💵 تتر (USDT): {usdt_toman:,} تومان\n\n"
    else:
        msg += "💵 تتر (USDT): ❌ (خطا در دریافت)\n\n"

    # قیمت ارزها
    msg += "💠 ارزهای دیجیتال (دلاری):\n"
    for k, v in crypto.items():
        if v is not None:
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
# زمان‌بندی ۲۴ ساعته
# -----------------------------
schedule.every(24).hours.do(send_update)

print("Bot is running...")

send_update()  # اولین پیام

while True:
    schedule.run_pending()
    time.sleep(1)
