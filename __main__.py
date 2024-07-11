import os
import asyncio

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from database.database import Database, User
from core import DelBot
from data import *
from routers import setup_routers

async def main():
    db = Database()
    logger : Logger = set_logger("KgtsBot", log_path="data/logs.log")

    dp = Dispatcher(storage=MemoryStorage())

    bot = DelBot(
        config = Config,
        database = db,
        logger = logger,
        dp = dp,
        user = User,
    )

    dp.startup.register(bot.on_startup)
    dp.shutdown.register(bot.on_shutdown)

    setup_routers(dp)

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        os.system("cls" if os.name == "nt" else "clear")
        asyncio.run(main())
    except KeyboardInterrupt:
        pass