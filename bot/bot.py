import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import dream
import api_keys_import as KEYS

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=KEYS.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(dream.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())