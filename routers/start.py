from aiogram import Router, Bot, types
from aiogram.filters import Command 

from keyboards import main_reply, admin_reply

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message, bot: Bot):
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
    await message.answer(reply_markup=main_reply())

@router.message(Command("start"), is_admin=True)
async def admin_handler(message: types.Message):

    await message.answer(reply_markup=admin_reply())