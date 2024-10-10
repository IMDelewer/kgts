from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

from keyboards import main_reply, admin_reply, subscribe_inline, rules_inline
from core import IsAdmin

router = Router()

WELCOME_MSG = """✨ *Добро пожаловать\!*
➖➖➖➖➖➖➖➖➖
Вас приветствует телеграмм бот *ОАО КГТС\!*

Если хотите получить помощь от оператора 🎧,
нажмите на кнопку "🎧 Поддержка" ниже\.👇
➖➖➖➖➖➖➖➖➖"""

ADMIN_MSG = """✨ *Добро пожаловать\!*
➖➖➖➖➖➖➖➖➖
Приветствую *администратор*\!
Для поиска нажмите на кнопки ниже\. 👇
➖➖➖➖➖➖➖➖➖
❗ `Это сообщение видят только администраторы\.`"""

SUBSCRIBE_MSG = """❌ *Вы не подписаны*
➖➖➖➖➖➖➖➖➖
*Подпишитесь на канал\.*
После, *нажмите на кнопку* '✅ Проверить'
➖➖➖➖➖➖➖➖➖"""

RULES_MSG = """📕 *Правила пользования*
➖➖➖➖➖➖➖➖➖➖➖
*1\.* Перед тем, как задать вопрос в поддержку,
проверьте есть ли этот вопрос в моей базе\.

*2\.* Если ваш вопрос не найдем в моей базе,
попробуйте перефразировать ваш вопрос\.

Для подтверждения правил нажмите на кнопку ниже\. 👇
➖➖➖➖➖➖➖➖➖➖➖"""

CHANNEL_ID = '-1002192731130'

async def check_user_subscription(message: Message, bot: Bot, user_level: int):
    if user_level == 0:
        user_status = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)
        if user_status.status != 'left':
            bot.db.update({"user_id": message.from_user.id}, {'$set': {"level": 1}})
        else:
            await message.answer(SUBSCRIBE_MSG, reply_markup=subscribe_inline(None))
    elif user_level == 1:
        await message.answer(RULES_MSG, reply_markup=rules_inline(message.from_user.id))
    elif user_level == 2:
        await message.answer(WELCOME_MSG, reply_markup=main_reply())

@router.message(Command(commands="start"))
async def start_handler(message: Message, bot: Bot):
    db = bot.db
    db.use_collection("users")
    
    user = db.find({"user_id": message.from_user.id})

    if user:
        await check_user_subscription(message, bot, user["level"])
    else:
        db.insert({
            "username": message.from_user.username,
            "user_id": message.from_user.id,
            "first_name": message.from_user.first_name,
            "second_name": message.from_user.last_name,
            "level": 0,
            "current_support": 0,
        })
        await check_user_subscription(message, bot, 0)
        db.update({"user_id": "stats"}, {"$set": {"users": db.find({"user_id": "stats"})["users"]+1}})

@router.message(Command(commands="admin"), IsAdmin())
async def admin_handler(message: Message):
    await message.answer(ADMIN_MSG, reply_markup=admin_reply())