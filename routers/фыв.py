from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from keyboards import support_inline
from database import Database

router = Router()

database = Database(current_collection='supports')

class Wait(StatesGroup):
    waiting_message = State()
    waiting_message_support = State()

@router.message(F.text == "🎧 Поддержка")
async def support_wait(message: Message, state: FSMContext):
    support_text = """🎧 Поддержка
➖➖➖➖➖➖➖➖➖
Задайте ваш вопрос ❓.
В ближайшее время оператор ответит Вам 🎧.
➖➖➖➖➖➖➖➖➖
"""
    await message.answer(support_text)
    await state.set_state(Wait.waiting_message)

@router.message(StateFilter(Wait.waiting_message))
async def support_handler(message: Message, state: FSMContext, bot: Bot):
    # Insert the support request into the database
    support_data = {
        'collection': 'supports',
        'request': message.text,
        'userid': message.from_user.id,
        'operid': 0,
        'rate': 0,
        'cancels': 0,
        'cancel_ids': [],
        'status': 'opened',
        'support_name': None
    }
    support = bot.db.insert(support_data)
    
    # Notify all operators
    operators = bot.db.find_all("access_lvl", 2, "users")
    for operator in operators:
        try:
            op = await bot.get_chat(chat_id=int(operator["user_id"]))
            await bot.send_message(
                chat_id=operator["user_id"],
                text=f"Новый запрос от клиента: {message.text}",
                reply_markup=support_inline(operator["user_id"])
            )
        except Exception as e:
            # Handle errors, such as user not found or other issues
            print(f"Error sending message to operator {operator['user_id']}: {e}")

    await state.clear()

@router.callback_query()
async def support_accept_reject_handler(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = callback.data.split("|")
    action, user_id = data[0], int(data[1])
    db = bot.db
    
    support = db.find_one("supports", {"userid": user_id})
    if not support:
        await callback.answer("Запрос не найден.")
        return
    
    if action == "reject":
        if support["operid"] == 0:
            if support["cancels"] < 4:
                if callback.from_user.id not in support["cancel_ids"]:
                    db.update("supports", {"userid": user_id}, {"$inc": {"cancels": 1}, "$push": {"cancel_ids": callback.from_user.id}})
                    await callback.answer("Запрос отклонен.")
                else:
                    await callback.answer("Похоже, вы уже отклонили этот запрос.")
            else:
                await callback.answer("Вы не можете отклонить этот запрос.")
        else:
            await callback.answer("Похоже, этот запрос уже приняли.")
    
    elif action == "accept":
        if support["operid"] == 0:
            db.update("supports", {"userid": user_id}, {"$set": {"operid": callback.from_user.id, "status": "accepted"}})
            await bot.send_message(chat_id=support["userid"], text="Ваш запрос был принят!")
            await callback.answer("Напишите ваш ответ на вопрос.")
            await state.set_state(Wait.waiting_message_support)
        else:
            await callback.answer("Похоже, этот запрос уже приняли.")

@router.message(StateFilter(Wait.waiting_message_support))
async def support_answer_handler(message: Message, state: FSMContext, bot: Bot):
    # Save the support answer
    # Note: You should implement a way to relate this answer to the specific support request.
    await message.answer("Ваш ответ записан.")
    await state.clear()
