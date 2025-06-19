import requests
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler

# CONFIG
API_KEY = "fa8c236ccb084bb3a54afed84e9c6ec4"
SYMBOL = "XAU/USD"
INTERVAL = "1min"
TELEGRAM_TOKEN = "7986463306:AAHa4T09RRlTcadiWADszvM_JUcY0ZG43yc"
CHAT_ID = "1991137917"

bot = Bot(token=TELEGRAM_TOKEN)

def get_price():
    url = f"https://api.twelvedata.com/time_series?symbol={SYMBOL}&interval={INTERVAL}&apikey={API_KEY}&outputsize=2"
    response = requests.get(url).json()
    try:
        data = response['values']
        close1 = float(data[0]['close'])
        close2 = float(data[1]['close'])

        if close1 > close2:
            send_signal(f"🟢 Buy Signal for {SYMBOL}\nCurrent Price: {close1}")
        elif close1 < close2:
            send_signal(f"🔴 Sell Signal for {SYMBOL}\nCurrent Price: {close1}")
        else:
            print("No change.")
    except Exception as e:
        print("Error:", e)

def send_signal(message):
    bot.send_message(chat_id=CHAT_ID, text=message)

# Scheduler
scheduler = BlockingScheduler()
scheduler.add_job(get_price, 'interval', minutes=1)  # every 1 minute
scheduler.start()
