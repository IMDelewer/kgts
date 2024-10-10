from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

from keyboards import support_inline, answer_inline, rate_inline

router = Router()

class Wait(StatesGroup):
    waiting_message = State()
    waiting_message_support = State()

SUPPORT_MESSAGE = """🎧 Поддержка
➖➖➖➖➖➖➖➖➖
❓ *Задайте ваш вопрос*
➖➖➖➖➖➖➖➖➖
"""

def answer_support(message):
    return f"""✒ Ответ
➖➖➖➖➖➖➖➖
{message}
➖➖➖➖➖➖➖➖
"""

async def send_message_to_user(bot, user_id, text, reply_markup=None):
    await bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)

@router.message(F.text == "🎧 Поддержка")
async def support_wait(message: Message, state: FSMContext):
    await message.answer(SUPPORT_MESSAGE)
    await state.set_state(Wait.waiting_message)

@router.message(StateFilter(Wait.waiting_message))
async def support_handler(message: Message, state: FSMContext, bot: Bot):
    db = bot.db
    db.use_collection("supports")

    await state.clear()

    support_data = {
        "id": len(list(db.find({}))),
        "request": message.text,
        "userid": message.from_user.id,
        "operid": 0,
        "rate": None,
        "cancels": 0,
        "cancel_ids": [],
        "status": "opened",
    }

    db.insert(support_data)

    db.use_collection("users")
    db.update({"user_id": message.from_user.id}, {"current_support": support_data["id"]})

    stats = db.find({"user_id": "stats"})[0]
    db.update(
        {"user_id": "stats"},
        {
            "all_supports_day": stats.get("all_supports_day", 0) + 1,
            "all_supports_mouth": stats.get("all_supports_mouth", 0) + 1,
            "all_supports": stats.get("all_supports", 0) + 1
        }
    )

    for operator in db.find({"level": 4}):
        await send_message_to_user(
            bot,
            operator["user_id"],
            f"❗ Новый запрос от клиента: '{message.text}'",
            reply_markup=support_inline(support_data["id"])
        )

@router.message(StateFilter(Wait.waiting_message_support))
async def support_answer_handler(message: Message, state: FSMContext, bot: Bot):
    db = bot.db


    db.use_collection("users")
    user_data = db.find({"user_id": message.from_user.id})[0]
    current_support_id = user_data["current_support"]

    db.use_collection("supports")
    support = db.find({"id": current_support_id})[0]

    if support:
        await send_message_to_user(
            bot,
            support["userid"],
            answer_support(message.text),
            reply_markup=answer_inline(message.from_user.id)
        )
        await message.answer("Ваш ответ записан и отправлен\.")
        
        db.update({"id": current_support_id}, {"status": "answered"})

        await state.clear()


        db.use_collection("users")
        db.update({"user_id": message.from_user.id}, {"current_support": 0})
