import os
import asyncio

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from core import *
from data import *
from routers import setup_routers

async def main():
    db = Database(db_name="kgts", uri="mongodb+srv://imdelwer:QJTz12cArDZoNiBi@tester.shecthy.mongodb.net/?retryWrites=true&w=majority&appName=tester")
    logger : Logger = set_logger("KgtsBot")

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    bot = DelBot(
        config = Config,
        database = db,
        logger = logger,
        dp = dp,
        helper = Helper,
    )

    dp.startup.register(bot.on_startup)
    dp.shutdown.register(bot.on_shutdown)

    setup_routers(dp, logger)

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        os.system("cls" if os.name == "nt" else "clear")
        asyncio.run(main())
    except KeyboardInterrupt:
        pass