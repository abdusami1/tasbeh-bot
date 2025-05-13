from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook
import logging
import os

API_TOKEN = os.getenv("BOT_TOKEN")

WEBHOOK_HOST = 'https://tasbeh-bot.onrender.com'
WEBHOOK_PATH = f'/webhook/{API_TOKEN}'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.environ.get('PORT', 5000))

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start'])
async def start_handler(message: Message):
    return SendMessage(message.chat.id, "Assalomu alaykum, tasbeh botga xush kelibsiz!")

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.delete_webhook()

if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
