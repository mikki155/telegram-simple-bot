import requests
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os

load_dotenv()

async def pollCryptoPrices(update: Update):
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin&price_change_percentage=1h"
    while True:
        response = requests.get(url).json()
        time.sleep(60)
        btc_change_1h = response[0]["price_change_percentage_1h_in_currency"]
        if abs(btc_change_1h) > 5:
            await update.message.reply_text("Bitcoin is on the move! "
                                            "1h percentage change: " + str(round(btc_change_1h, 2)) +
                                            " " +
                                            "https://coin-images.coingecko.com/coins/images/1/large/bitcoin.png?1696501400")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Starting to poll cryptocurrency data...')
    await pollCryptoPrices(update)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a simple bot that polls price data every 15 minutes,'
                                    'and shoots a notification if there is a big move.')

def main():

    application = Application.builder().token(os.getenv('BOT_TOKEN')).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()