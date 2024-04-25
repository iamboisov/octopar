from aiogram import Router, F, types, Bot
from aiogram.types import Message
from aiogram.filters import Command
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
import time
import api_keys_import as KEYS
import db_functions.crud as db
import asyncio


router = Router()
bot = Bot(token=KEYS.BOT_TOKEN)
MIN_LENGTH = 140

# Первый запуск бота
@router.message(Command("start"))
async def start(message: types.Message):
    # Определение данных пользователя
    user_id = message.chat.id
    name = message.from_user.first_name
    telegram_username = message.from_user.username
    existing_user = await db.collection.find_one({"_id": user_id})

    # Проверка пользователя в базе данных
    if not existing_user:
        await db.add_user(user_id, name, telegram_username)
        await message.answer("Привет! Это толкователь снов с ИИ. Какой сон тебе приснился?")
    else:
        await message.answer("С возвращением! Какой сон тебе приснился?")

    await db.update_user(user_id, name, telegram_username)


# Сообщение от пользователя
@router.message(F.text)
async def send_answer(message: Message):
    sent_message = await message.answer(f"Толкую...⏳")
    user_id = message.chat.id
    name = message.from_user.first_name
    telegram_username = message.from_user.username
    await db.update_user(user_id, name, telegram_username)

    await asyncio.sleep(4)

    gigachat = GigaChat(credentials=KEYS.GIGACHAT_KEY, verify_ssl_certs=False)
    messages = [
        SystemMessage(content="Перефразируй и напиши 3 детальных толкования сна. В конце укажи '🔮 Предсказание:' и напиши необычное предсказание на неделю."),
        HumanMessage(content=message.text)
    ]
    res = gigachat(messages)
    print(res.content)

    if len(res.content) < MIN_LENGTH:
        await message.answer("Мы придерживаемся политики, которая запрещает: Насилие, Оскорбления, Открытая Сексуализация.\n\nСтарайтесь избегать слов, которые содержат оскорбительный характер. \n\nСпасибо за понимание!🐑")
    else:
        await message.answer(res.content)

    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)