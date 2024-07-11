from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(F.text == '💡 О роботе')
async def info_message(message: Message, bot: Bot):
    info = f"""💡 О роботе
➖➖➖➖➖➖➖➖
Это оффициальный бот поддержки созданный для ОАО "КГТС" 
ТГ Создателей : @imdelewer
Версия : {bot.config.version}
➖➖➖➖➖➖➖➖
"""
    await message.answer(info)