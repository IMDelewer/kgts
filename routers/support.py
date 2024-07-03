from aiogram import Router, Bot
from aiogram.F import text, data
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards import support_inline

router = Router()
class Wait(StatesGroup):
    waiting_message = State()
    waiting_message_support = State()

@router.message(text == "🎧 Поддержка")
async def support_wait(message: Message):
    await Wait.waiting_message.set()

@router.message(State=Wait.waiting_message)
async def support_handler(message: Message, state: FSMContext, bot : Bot):
    database = bot.db
    data = {
        "request" : message.text,
        "userid" : message.from_user.id,
        "operid" : 0,
        "rate" : 0,
        "cancels" : 0,
        "cancel_ids": [],
        "status": "opened",
        "sup_name" : None
    }
    await state.finish()
    database.insert(data)
    database.use_collenction("users")

    for support in database.find({"status": 1}):
        await bot.send_message(text=f"Новый запрос! {message.text}", chat_id=support["userid"], reply_markup=support_inline(data["userid"]))

@router.callback_query()
async def support_accept_reject_handler(callback: CallbackQuery, bot: Bot):
    data = callback.data.split("|")
    database = bot.db
    if data[0] == "reject":
        database.use_collection("supports")
        support = database.find({"userid": data[1]})
        if support["operid"] == 0:
            await callback.answer("Похоже, этот запрос уже приняли.")
        else:
            if support["cancels"] < 4:
                if callback.from_user.id not in support["cancel_ids"]:
                    support.insert({"cancels": support["cancels"]+1})
                    support.insert({"cancel_ids": support["cancel_ids"].append(callback.from_user.id)})
                else:
                    await callback.answer("Похоже, вы уже отклонили этот запрос.")
            else:
                await callback.answer("Вы не можете отклонить этот запрос")
    else:
        database.use_collection("supports")
        support = database.find({"userid": data[1]})
        support.insert({"operid": callback.from_user.id})
        support.insert({"status": "accepted"})
        bot.send_message(text="Ваш запрос был принят!", chat_id=support["userid"])
        callback.answer("Напишите ваш ответ на вопрос")
        await Wait.waiting_message_support.set()

@router.message(State=Wait.waiting_message_support)
async def support_answer_handler(message: Message, state: FSMContext, bot: Bot):
    print("asda")