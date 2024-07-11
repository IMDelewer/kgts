from aiogram import Router, Bot, types, F
from aiogram.filters import Command 

from keyboards import main_reply, admin_reply
from data import Config

router = Router()

@router.message(Command(commands="start"))
async def start_handler(message: types.Message, bot: Bot):
    if message.from_user.id not in Config.admins:
        welcome = """✨ Добро пожаловать!
➖➖➖➖➖➖➖➖➖
Вас приветствует телеграмм бот ОАО КГТС!

Если хотите получить помощь от опертатора 🎧,
нажмите на кнопку "🎧 Поддержка" ниже.👇
➖➖➖➖➖➖➖➖➖"""

        database = bot.db
        database.use_collection("users")
        if database.find({"userid": message.from_user.id}):
            pass
        else:
            data = {
                "username": message.from_user.username,
                "first_name": message.from_user.first_name,
                "second_name": message.from_user.last_name,
                "userid": message.from_user.id,
                "chatid": f"{message.chat.id}",
                "level": 0,
                "is_prem": message.from_user.is_premium,
                
            }
            database.insert(data)
        await message.answer(welcome, reply_markup=main_reply())
    elif message.from_user.id in Config.admins:
        admin = """✨ Добро пожаловать!
➖➖➖➖➖➖➖➖➖
Приветствую администратор!

Для поиска нажмите на кнопки ниже. 👇
➖➖➖➖➖➖➖➖➖
❗ Это сообщение видят только администраторы."""
    await message.answer(text=admin, reply_markup=admin_reply())
