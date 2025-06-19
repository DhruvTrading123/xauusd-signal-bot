import os
import time
import requests
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# ✅ Get from environment
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")  # This should be your Telegram user ID

# --- Get XAUUSD Price ---
def get_xauusd_price():
    try:
        response = requests.get("https://api.metals.live/v1/spot")
        data = response.json()
        for item in data:
            if "gold" in item:
                return float(item["gold"])
    except Exception as e:
        print("Error getting price:", e)
        return None

# --- Generate Trade Signal ---
def generate_signal(price):
    if price is None:
        return "❌ Error getting XAUUSD price"
    elif price < 2300:
        return f"💹 BUY XAUUSD @ {price} (Support Zone)"
    elif price > 2350:
        return f"📉 SELL XAUUSD @ {price} (Resistance Zone)"
    else:
        return f"⚠️ Wait — No clear signal at {price}"

# --- /start Command ---
def start(update: Update, context: CallbackContext):
    update.message.reply_text("🤖 Bot is live! Use /signal to get a trade idea.")

# --- /signal Command ---
def signal(update: Update, context: CallbackContext):
    price = get_xauusd_price()
    sig = generate_signal(price)
    update.message.reply_text(sig)

# --- Start the Bot ---
def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("signal", signal))

    # ✅ Auto send signal on startup
    price = get_xauusd_price()
    msg = generate_signal(price)
    updater.bot.send_message(chat_id=CHAT_ID, text=f"📡 Bot Started\n\n{msg}")

    updater.start_polling()
    print("🚀 Bot running...")
    updater.idle()

if __name__ == "__main__":
    main()
