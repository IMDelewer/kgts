from aiogram import Router, Bot, types
from aiogram.filters import Command 

from keyboards import main_reply

router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message, bot: Bot):
    database = bot.db
    
    database.use_collection("users")

    welcome_message = """привет
"""

    await message.answer(welcome_message, reply_markup=main_reply())
    
