# import os
# import asyncio
# from datetime import datetime
# from aiogram import Bot, Dispatcher, types, Router, F
# from aiogram.filters import Command, CommandObject, CommandStart
# import motor.motor_asyncio
# from langchain.schema import HumanMessage, SystemMessage
# from langchain.chat_models.gigachat import GigaChat
# import time

# MONGODB_URI = os.getenv('MONGODB_URI')
# BOT_TOKEN = os.getenv('BOT_TOKEN')
# GIGACHAT_KEY = os.getenv('GIGACHAT_API_KEY')

# bot = Bot(token=BOT_TOKEN)
# dp = Dispatcher()
# router = Router()
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

# @router.message(Command("start"))
# async def start(message: types.Message):
#     user_id = message.chat.id
#     name = message.from_user.first_name
#     telegram_username = message.from_user.username
#     existing_user = await collection.find_one({"_id": user_id})
#     if not existing_user:
#         await add_user(user_id, name, telegram_username)
#     await message.answer("Привет! Это толкователь снов с ИИ. Напиши свой сон, а я его растолкую")
#     await update_user(user_id, name, telegram_username)

# @router.message(F.text)
# async def send_answer(message: types.Message):
#     for x in range(5):
#         time.sleep(1)
#         await message.answer(f"Толкую...{x}")
#     chat = GigaChat(credentials=GIGACHAT_KEY, verify_ssl_certs=False)
#     messages = [
#         SystemMessage(
#             content="Перефразируй и растолкуй сон детально. Если сон грустный, то дай грустное толкование. Если сон хороший, то дай радостное толкование."
#         ),
#         HumanMessage(content=message.text)
#     ]
#     res = chat(messages)
#     print(res.content)
#     await message.answer(res.content)

# async def main():
#     dp.include_router(router)
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     asyncio.run(main())
