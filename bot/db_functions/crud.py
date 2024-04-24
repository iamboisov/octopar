import motor.motor_asyncio
from datetime import datetime
import api_keys_import as KEYS

cluster = motor.motor_asyncio.AsyncIOMotorClient(KEYS.MONGODB_URI)
collection = cluster.DreamBot.User_Auth


# Добавление пользователя в БД
async def add_user(user_id, username, telegram_username):
    date = datetime.now()
    user_data = {
        "_id": user_id,
        "name": str(username),
        "first_seen": date,
        "last_seen": date,
        "telegram_username": "@" + str(telegram_username) if telegram_username else None
    }
    await collection.insert_one(user_data)


# Обновление данных по пользователю
async def update_user(user_id, username, telegram_username):
    date = datetime.now()
    user_data = {
        "last_seen": date,
        "name": str(username)
    }
    if telegram_username:
        user_data["telegram_username"] = "@" + str(telegram_username)

    await collection.update_one(
        {"_id": user_id},
        {"$set": user_data}
    )