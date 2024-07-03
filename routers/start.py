from aiogram import Router, Bot, types
from aiogram.filters import Command 

from keyboards import main_reply, admin_reply
from core import IsAdmin

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message, bot: Bot):
    welcome = """✨ Добро пожаловать!
➖➖➖➖➖➖➖➖➖
Вас приветствует телеграмм бот ОАО КГТС!

Если хотите получить помощь от опертатора 🎧,
нажмите на кнопку "🎧 Поддержка" ниже.👇
➖➖➖➖➖➖➖➖➖
"""

    database = bot.db
    database.use_collection("users")
    if database.find({"userid": message.from_user.id}):
        pass
    else:
        data = {
            "username": message.from_user.username,
            "userid": message.from_user.id,
            "level": 0,
            "is_prem": message.from_user.is_premium,
            "first_name": message.from_user.first_name,
            "second_name": message.from_user.last_name
        }
        database.insert(data)
    await message.answer(welcome, reply_markup=main_reply())

@router.message(IsAdmin(), Command("str"))
async def admin_handler(message: types.Message):
    admin = """✨ Добро пожаловать!
➖➖➖➖➖➖➖➖➖
Приветствую администратор!

Для поиска нажмите на кнопки ниже. 👇
➖➖➖➖➖➖➖➖➖
❗ Это сообщение видят только администраторы.
"""
    await message.answer(admin, reply_markup=admin_reply())