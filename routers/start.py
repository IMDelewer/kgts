from aiogram import Router, Bot, types, F
from aiogram.filters import Command 

from keyboards import main_reply, admin_reply
from data import Config

from database.database import User

router = Router()

@router.message(Command(commands="start"))
async def start_handler(message: types.Message, bot: Bot):

    user = bot.user(
            collection = 'users',
            username = message.from_user.username,
            user_id = message.from_user.id,
            first_name = message.from_user.first_name,
            second_name =  message.from_user.last_name,
        )
    
    try:
        await user.insert()
    except Exception as e:
        bot.logger.error(e)
