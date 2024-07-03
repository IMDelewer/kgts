from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(F.text == '💡 О роботе')
async def info_message(message: Message, bot: Bot):
    info = f"""💡 О роботе
➖➖➖➖➖➖➖➖
Это оффициальный бот поддержки созданный для ОАО "КГТС" 
Создатель : /delewer
Версия : {bot.config.version}
➖➖➖➖➖➖➖➖
"""
    await message.answer(info)

@router.message(Command("delewer"))
async def delewer_message(message: Message):
    creater = f"""⭐ Создатель
➖➖➖➖➖➖➖➖➖➖
Здравстуйте, я создатель этого робота.
Связаться со мной можно здесь :

Email : delewer@asphr.xyz
Телеграмм : @imdelewer , @deleweer
➖➖➖➖➖➖➖➖➖➖
"""
    await message.answer(creater)