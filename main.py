from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
import asyncio
import logging
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())