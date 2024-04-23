from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart
import os
import time



router = Router()


@router.message(Command("adminstats"))
async def check_stats(message: types.Message):
    if message.from_user.id in (5233833942):
        await message.answer("Привет, Амир!")
    else:
        await message.answer("Ты не админ!")