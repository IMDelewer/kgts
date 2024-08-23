from aiogram import Router, Bot, types, F
from aiogram.filters import Command 

from keyboards import main_reply #admin_reply
from data import Config

from database.database import User

router = Router()

welcome = """✨ Добро пожаловать!
➖➖➖➖➖➖➖➖➖
Вас приветствует телеграмм бот ОАО КГТС!

Если хотите получить помощь от опертатора 🎧,
нажмите на кнопку "🎧 Поддержка" ниже.👇
➖➖➖➖➖➖➖➖➖"""

# admin = """✨ Добро пожаловать!
# ➖➖➖➖➖➖➖➖➖
# Приветствую администратор!

# Для поиска нажмите на кнопки ниже. 👇
# ➖➖➖➖➖➖➖➖➖
# ❗ Это сообщение видят только администраторы."""

@router.message(Command(commands="start"))
async def start_handler(message: types.Message, bot: Bot):

    #if message.from_user.id not in Config.admins:
        user = bot.user(
                collection = 'users',
                username = message.from_user.username,
                user_id = message.from_user.id,
                first_name = message.from_user.first_name,
                second_name =  message.from_user.last_name,
            )

        await user.insert()

        await message.answer(welcome, reply_markup=main_reply())

    # elif message.from_user.id in Config.admins:
    #     await message.answer(admin, reply_markup=admin_reply())