import os
from asyncio import run
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from core import DelBot, Database
from data import Config, set_logger
from routers import setup_routers

def reset_supports(db):
    db.use_collection("users")
    db.update({"level": 4}, {"day_supports": 0}, many=True)
    db.update({"user_id": "stats"}, {"all_day_supports": 0})

def reset_monthly_supports(db):
    db.use_collection("users")
    db.update({"level": 4}, {"mouth_supports": 0}, many=True)
    db.update({"user_id": "stats"}, {"all_mouth_supports": 0})

def info_database(db):

    db.use_collection("users")
    if db.find({"user_id": "stats"}):
        pass
    else:
        db.insert({
            "user_id": "stats",
            "users": 0,
            "all_rate": 0,
            "plus_rate": 0,
            "minus_rate": 0,
            "all_supports_day": 0,
            "all_supports_mouth": 0,
            "all_supports": 0
        })

async def main():
    scheduler = BackgroundScheduler()
    db = Database(Config.db_name, Config.url)
    logger = set_logger("KgtsBot", log_path="data/logs.log")
    
    dp = Dispatcher(storage=MemoryStorage())
    bot = DelBot(config=Config, database=db, logger=logger, dp=dp)

    dp.startup.register(bot.on_startup)
    dp.shutdown.register(bot.on_shutdown)

    scheduler.add_job(reset_supports, 'cron', hour=0, minute=0, args=[db])
    scheduler.add_job(reset_monthly_supports, 'cron', day=1, hour=0, minute=0, args=[db])

    setup_routers(dp)
    info_database(db)

    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        os.system("cls" if os.name == "nt" else "clear")
        run(main())
    except KeyboardInterrupt:
        pass
