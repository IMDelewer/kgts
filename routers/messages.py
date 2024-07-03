from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start_message(message: Message):
    welcome = """✨ Добро пожаловать!
➖➖➖➖➖➖➖➖➖
Вас приветствует телеграмм бот ОАО КГТС!

Если хотите получить помощь от опертатора 🎧,
нажмите на кнопку "🎧 Поддержка" ниже.👇
➖➖➖➖➖➖➖➖➖
"""
    await message.answer(welcome)

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

# @router.message(Command("start"))
# async def admin_message(message: Message):
#     admin = """✨ Добро пожаловать!
# ➖➖➖➖➖➖➖➖➖
# Приветствую администратор!

# Для поиска нажмите на кнопки ниже. 👇
# ➖➖➖➖➖➖➖➖➖
# ❗ Это сообщение видят только администраторы.
# """
#     await message.answer(admin)

@router.message(F.text == "🎧 Поддержка")
async def support_message(message: Message):
    support = """🎧 Поддержка
➖➖➖➖➖➖➖➖➖
Задайте ваш вопрос ❓.
В ближайшее время оператор ответит Вам 🎧.
➖➖➖➖➖➖➖➖➖
"""
    await message.answer(support)

@router.message(F.text == "❓ FAQ")
async def faq_message(message: Message):
    faq = """❓ FAQ
➖➖➖➖➖➖➖➖➖
Задайте ваш вопрос ❓.
Я поищу его в моей базе 🔍.
➖➖➖➖➖➖➖➖➖
"""
    await message.answer(faq)