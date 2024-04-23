from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
import os
import time

GIGACHAT_KEY = os.getenv('GIGACHAT_API_KEY')

router = Router()


@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Это толкователь снов с ИИ. Напиши свой сон, а я его растолкую")

@router.message(F.text)
async def send_answer(message: Message):
    for x in reversed(range(5)):
        time.sleep(1)
        await message.answer(f"Толкую...{x}")
    chat = GigaChat(credentials=GIGACHAT_KEY, verify_ssl_certs=False)
    messages = [
        SystemMessage(
            content="Перефразируй и растолкуй сон детально. Если сон грустный, то дай грустное толкование. Если сон хороший, то дай радостное толкование."
        )
    ]
    messages.append(HumanMessage(content=message.text))
    res = chat(messages)
    messages.append(res)
    print(res.content)
    await message.answer(res.content)