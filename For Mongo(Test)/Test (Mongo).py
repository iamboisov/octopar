# from aiogram import Bot, Dispatcher, types
# import motor.motor_asyncio
# import asyncio
# import os
# from datetime import datetime

# MONGODB_URI = os.getenv('MONGODB_URI')
# BOT_TOKEN = os.getenv('BOT_TOKEN')

# bot = Bot(token=BOT_TOKEN)
# dp = Dispatcher()

# cluster = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
# collection = cluster.DreamBot.User_Auth

# async def add_user(user_id, username, telegram_username):
#     date = datetime.now().date()
#     user_data = {
#         "_id": user_id,
#         "name": str(username),
#         "last_seen": str(date),
#         "telegram_username": "@" + str(telegram_username) if telegram_username else None
#     }
#     await collection.insert_one(user_data)

# async def update_user(user_id, username, telegram_username):
#     date = datetime.now().date()
#     user_data = {
#         "last_seen": str(date),
#         "name": str(username)
#     }
#     if telegram_username:
#         user_data["telegram_username"] = "@" + str(telegram_username)

#     await collection.update_one(
#         {"_id": user_id},
#         {"$set": user_data}
#     )

# @dp.message()
# async def handle_messages(message: types.Message):
#     user_id = message.chat.id
#     name = message.from_user.first_name
#     telegram_username = message.from_user.username

#     if message.text and message.text.startswith('/start'):
#         existing_user = await collection.find_one({"_id": user_id})
#         if not existing_user:
#             await add_user(user_id, name, telegram_username)
#             await bot.send_message(message.chat.id, "Привет, какой сон тебе приснился?")
#         else:
#             await bot.send_message(message.chat.id, "С возвращением! Какой сон тебе приснился?")
    
#     await update_user(user_id, name, telegram_username)

# async def main():
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     asyncio.run(main())

