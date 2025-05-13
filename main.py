import logging
import json
import os
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from dotenv import load_dotenv

load_dotenv()  # .env fayldan o‘qish

API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}
DATA_FILE = "data.json"

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(user_data, f)

def load_data():
    global user_data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            user_data = json.load(f)

load_data()

# Klaviatura
menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(KeyboardButton("Tasbeh+"))
menu.add(KeyboardButton("0 ga qaytarish"), KeyboardButton("Zikrini almashtirish"))
menu.add(KeyboardButton("Statistika"))

# /start komandasi
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user_id = str(message.from_user.id)
    username = message.from_user.username or "no_username"
    if user_id not in user_data:
        user_data[user_id] = {"zikr": "Subhanalloh", "hisob": {}, "count": 0}
        save_data()
        await bot.send_message(chat_id=ADMIN_ID, text=f"Yangi foydalanuvchi: @{username} (ID: {user_id})")
    await message.answer("Assalomu alaykum, tasbeh botga xush kelibsiz!", reply_markup=menu)

# Tasbeh+
@dp.message_handler(Text(equals="Tasbeh+"))
async def tasbeh_plus(message: types.Message):
    user_id = str(message.from_user.id)
    today = datetime.now().strftime("%d.%m.%Y")
    zikr = user_data[user_id]["zikr"]
    user_data[user_id]["count"] += 1
    if today not in user_data[user_id]["hisob"]:
        user_data[user_id]["hisob"][today] = {}
    if zikr not in user_data[user_id]["hisob"][today]:
        user_data[user_id]["hisob"][today][zikr] = 0
    user_data[user_id]["hisob"][today][zikr] += 1
    save_data()
    await message.answer(f"{zikr}: {user_data[user_id]['hisob'][today][zikr]}")
    await bot.send_message(chat_id=ADMIN_ID, text=f"{user_id} | {zikr} | +1")

# 0 ga qaytarish
@dp.message_handler(Text(equals="0 ga qaytarish"))
async def reset_counter(message: types.Message):
    user_id = str(message.from_user.id)
    user_data[user_id]["count"] = 0
    save_data()
    await message.answer("Hisob qayta tiklandi")
    await bot.send_message(chat_id=ADMIN_ID, text=f"{user_id} hisobni 0 ga tushirdi")

# Zikrni almashtirish
@dp.message_handler(Text(equals="Zikrini almashtirish"))
async def change_zikr(message: types.Message):
    user_id = str(message.from_user.id)
    old = user_data[user_id]["zikr"]
    new = "Alhamdulillah" if old == "Subhanalloh" else "Allohu Akbar" if old == "Alhamdulillah" else "Subhanalloh"
    user_data[user_id]["zikr"] = new
    save_data()
    await message.answer(f"Yangi zikr: {new}")
    await bot.send_message(chat_id=ADMIN_ID, text=f"{user_id} zikrni o'zgartirdi: {old} -> {new}")

# Statistika
@dp.message_handler(Text(equals="Statistika"))
async def show_stats(message: types.Message):
    user_id = str(message.from_user.id)
    stat_text = "Statistika:\n"
    for sana, zikrlar in user_data[user_id]["hisob"].items():
        stat_text += f"\n{sana}:\n"
        for zikr, soni in zikrlar.items():
            stat_text += f"  {zikr}: {soni}\n"
    await message.answer(stat_text)

# Har qanday xabar adminga yuboriladi
@dp.message_handler(content_types=types.ContentType.ANY)
async def echo_all(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "no_username"
    content = f"Xabar: {message.content_type}\nID: {user_id}\nUsername: @{username}"
    await bot.send_message(chat_id=ADMIN_ID, text=content)
    await bot.forward_message(chat_id=ADMIN_ID, from_chat_id=message.chat.id, message_id=message.message_id)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
