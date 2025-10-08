import logging
import os

import asyncio

from dotenv import load_dotenv

from aiogram import Dispatcher
from aiogram.types import BotCommand
from aiogram import Bot

from src.telegram_bot.routers import command_start, share_location_route

# todo: Необходимо реализовать через класс.

load_dotenv()

logging.basicConfig(level=logging.INFO)

# Создаём экземпляр бота
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()


async def main():
    dp.include_router(command_start)
    dp.include_router(share_location_route)
    try:
        async with bot:
            await bot.set_my_commands(
                commands=[
                    BotCommand(command='start', description='Старт'),
                    BotCommand(command='share_location', description='Отправить координаты'),
                ],
            )
            await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
