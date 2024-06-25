from aiogram import Router, Bot, types
from aiogram.filters import Command 

from keyboards import main_reply, admin_reply

router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message, bot: Bot):
    database = bot.db
    
    database.use_collection("users")

    welcome_message = """✨ Добро пожаловать!
'➖➖➖➖➖➖
Вас приветствует телеграмм бот ОАО КГТС!

Если хотите получить помощь от опертатора 🎧,
нажмите на кнопку "🎧 Поддержка" ниже.👇
"""

    await message.answer(welcome_message, reply_markup=admin_reply())
    
