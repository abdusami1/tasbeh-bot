from aiogram import Bot, Dispatcher, types, executor

API_TOKEN = '7770956707:AAEhptjrX5d_LrFh63toMMbd_45a0aYN4ks'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Assalomu alaykum, tasbeh botga xush kelibsiz!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
