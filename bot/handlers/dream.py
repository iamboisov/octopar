from aiogram import Router, F, types, Bot
from aiogram.types import Message
from aiogram.filters import Command
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
import time
import api_keys_import as KEYS
import db_functions.crud as db


router = Router()
bot = Bot(token=KEYS.BOT_TOKEN)


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
    # Лоадер
    sent_message = await message.answer(f"Толкую...⏳")
    for x in range(5):
        time.sleep(1)

    # Запрос к Гигачату
    gigachat = GigaChat(credentials=KEYS.GIGACHAT_KEY, verify_ssl_certs=False)
    messages = [
        SystemMessage(
            content="Перефразируй и растолкуй сон детально. Если сон грустный, то дай грустное толкование. Если сон хороший, то дай радостное толкование."
        ),
        HumanMessage(content=message.text)
    ]
    # messages.append()
    res = gigachat(messages)
    # messages.append(res)
    print(res.content)
    await message.answer(res.content)

    # Удаляем лоадер
    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)