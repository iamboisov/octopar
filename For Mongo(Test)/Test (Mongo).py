from aiogram import Bot, Dispatcher, types
import motor.motor_asyncio
import asyncio
import os
from datetime import datetime


MONGODB_URI = os.getenv('MONGODB_URI')
BOT_TOKEN = os.getenv('BOT_TOKEN')


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

cluster = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
collection = cluster.DreamBot.User_Auth

async def add_user(user_id):
    date = datetime.now().date()
    existing_user = await collection.find_one({"_id": user_id})
    if not existing_user:
        await collection.insert_one({
            "_id": user_id,
            "date": str(date)
        })
    else:
        print("Пользователь уже существует")
        # Позже можно сделать функцию update_user, чтобы обновлять инфу о юзерах которые снова используют /start 


@dp.message()
async def handle_messages(message: types.Message):
    if message.text and message.text.startswith('/start'):
        await bot.send_message(message.chat.id, "Привет, какой сон тебе приснился?")
        user_id = message.chat.id
        await add_user(user_id)

async def main():
    # Начать поллинг событий
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



