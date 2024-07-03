from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

from keyboards import support_inline

router = Router()

class Wait(StatesGroup):
    waiting_message = State()
    waiting_message_support = State()

@router.message(F.text == "🎧 Поддержка")
async def support_wait(message: Message, state: FSMContext):
    await state.set_state(Wait.waiting_message)
    await message.answer("Пожалуйста, опишите вашу проблему.")

@router.message(StateFilter(Wait.waiting_message))
async def support_handler(message: Message, state: FSMContext, bot: Bot):
    database = bot.db
    data = {
        "request": message.text,
        "userid": message.from_user.id,
        "operid": 0,
        "rate": 0,
        "cancels": 0,
        "cancel_ids": [],
        "status": "opened",
        "sup_name": None
    }
    await state.finish()
    database.insert(data)
    database.use_collection("users")

    for support in database.find({"status": 1}):
        await bot.send_message(
            text=f"Новый запрос! {message.text}",
            chat_id=support["userid"],
            reply_markup=support_inline(data["userid"])
        )

@router.callback_query()
async def support_accept_reject_handler(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = callback.data.split("|")
    database = bot.db
    if data[0] == "reject":
        database.use_collection("supports")
        support = database.find_one({"userid": int(data[1])})
        if support and support["operid"] == 0:
            if support["cancels"] < 4:
                if callback.from_user.id not in support["cancel_ids"]:
                    database.update_one(
                        {"userid": int(data[1])},
                        {"$inc": {"cancels": 1}, "$push": {"cancel_ids": callback.from_user.id}}
                    )
                    await callback.answer("Запрос отклонен.")
                else:
                    await callback.answer("Похоже, вы уже отклонили этот запрос.")
            else:
                await callback.answer("Вы не можете отклонить этот запрос.")
        else:
            await callback.answer("Похоже, этот запрос уже приняли.")
    else:
        database.use_collection("supports")
        support = database.find_one({"userid": int(data[1])})
        if support and support["operid"] == 0:
            database.update_one(
                {"userid": int(data[1])},
                {"$set": {"operid": callback.from_user.id, "status": "accepted"}}
            )
            await bot.send_message(text="Ваш запрос был принят!", chat_id=support["userid"])
            await callback.answer("Напишите ваш ответ на вопрос.")
            await state.set_state(Wait.waiting_message_support)
        else:
            await callback.answer("Похоже, этот запрос уже приняли.")

@router.message(StateFilter(Wait.waiting_message_support))
async def support_answer_handler(message: Message, state: FSMContext, bot: Bot):
    # Логика ответа на запрос поддержки
    await message.answer("Ваш ответ записан.")
    await state.finish()
