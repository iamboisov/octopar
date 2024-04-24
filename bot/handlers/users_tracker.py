from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import motor.motor_asyncio
from datetime import datetime
import api_keys_import as KEYS


router = Router()
cluster = motor.motor_asyncio.AsyncIOMotorClient(KEYS.MONGODB_URI)
collection = cluster.DreamBot.User_Auth



# Всего пользователей
async def users_all():
    all_users = await collection.distinct("_id")
    return len(all_users)


# Кол-во регистраций с начала месяца
async def users_month():
    start_of_month = datetime(datetime.now().year, datetime.now().month, 1).date()
    print(start_of_month)
    query = {"first_seen": {"$gte": str(start_of_month)}}
    month_users = collection.find(query)
    result = list()
    async for user in month_users:
        result.append(user)
    return len(result)


# Кол-во регистраций сегодня
async def users_day():
    today = datetime.now().date()
    query = {"first_seen": {"$eq": str(today)}}
    month_users = collection.find(query)
    result = list()
    async for user in month_users:
        result.append(user)
    return len(result)


# Кол-во использований сегодня
async def active_users_day():
    today = datetime.now().date()
    query = {"last_seen": {"$eq": str(today)}}
    month_users = collection.find(query)
    result = list()
    async for user in month_users:
        result.append(user)
    return len(result)



@router.message(Command("adminstats", prefix="%"))
async def check_stats(message: Message):
    if message.from_user.id in (5233833942, 980315710):
        await message.answer(
            "Привет, Админ!\n"\
            f"Регистраций (всего): {await users_all()}\n"\
            f"Пользователей за {datetime.now().month} месяц года: {await users_month()}\n"\
            f"Регистраций сегодня: {await users_day()}\n"\
            f"Активных пользователей сегодня: {await active_users_day()}"\
            )
    else:
        await message.answer("Ты не админ!")



