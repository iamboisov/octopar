import asyncio
import logging
from aiogram import Bot, Dispatcher
import os
from handlers import dream, users_tracker

BOT_TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=KEYS.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_routers(users_tracker.router, dream.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())