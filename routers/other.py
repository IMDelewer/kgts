from aiogram import Router, Bot, types, F
from aiogram.filters import Command

router = Router()

@router.message(F.text == '💡 О роботе')
async def otzivi_handler(message: types.Message, bot: Bot):
    mes = f"""💡 О роботе
➖➖➖➖➖➖➖➖
Это оффициальный бот поддержки созданный для ОАО "КГТС" 
Создатель : /delewer
Версия : {bot.config.version}
➖➖➖➖➖➖➖➖
"""
    await message.answer(mes)

@router.message(Command("delewer"))
async def delewer_handler(message: types.Message, bot: Bot):
    mes = f"""⭐ Создатель
➖➖➖➖➖➖➖➖➖➖
Здравстуйте, я создатель этого робота.
Связаться со мной можно здесь :

Email : delewer@asphr.xyz
Телеграмм : @imdelewer , @deleweer
➖➖➖➖➖➖➖➖➖➖
"""
    await message.answer(mes)