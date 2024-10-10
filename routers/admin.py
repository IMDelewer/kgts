from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

from core import IsAdmin
from keyboards import user_inline

router = Router()

class Wait(StatesGroup):
    waiting_user = State()
    waiting_support = State()

search_user_message = """🔍 Поиск юзера
➖➖➖➖➖➖➖➖
Отправьте *@юзернейм*, *айди* либо *имя* юзера
➖➖➖➖➖➖➖➖"""

search_support_message = """🔍 Поиск поддержки
➖➖➖➖➖➖➖➖
Отправьте *айди* поддержки
➖➖➖➖➖➖➖➖"""

def search_user_mes(user):
    message = f"""👤 Юзер
➖➖➖➖➖➖➖➖
Айди: {user["user_id"]}
Юзернейм: @{user.get('username', 'Не указан')}
Имя: {user["first_name"]}
Фамилия: {user["second_name"]}
Уровень доступа: {user["level"]}
Текущая поддержка: {user["current_support"]}
➖➖➖➖➖➖➖➖"""
    return message

def search_support_mes(support):
    status_map = {
        "opened": "Открыт",
        "accepted": "Принят",
        "answered": "Отвечен",
        "rated": "Получен отзыв"
    }

    star_map = {
        "one_star": "⭐",
        "two_stars": "⭐⭐",
        "three_stars": "⭐⭐⭐",
        "four_stars": "⭐⭐⭐⭐",
        "five_stars": "⭐⭐⭐⭐⭐"
    }

    message = f"""🔧 Поддержка
➖➖➖➖➖➖➖➖
Айди: {support["id"]}
Запрос: {support["request"]}
Юзер айди: @{support["userid"]}
Оператор айди: {support["operid"]}
Отзыв: {star_map.get(support["rate"])}
Айди отказавших: {support["level"]}
Статус: {status_map.get(support["status"])}
➖➖➖➖➖➖➖➖"""

    return message

@router.message(F.text == "🔍 Поиск юзера", IsAdmin())
async def search_user_wait(message: Message, state: FSMContext):
    await message.answer(search_user_message)
    await state.set_state(Wait.waiting_user)

@router.message(F.text == "🔍 Поиск поддержки", IsAdmin())
async def search_user_wait(message: Message, state: FSMContext):
    await message.answer(search_support_message)
    await state.set_state(Wait.waiting_support)

@router.message(StateFilter(Wait.waiting_user), IsAdmin())
async def search_user_handler(message: Message, state: FSMContext, bot: Bot):
    db = bot.db
    db.use_collection("users")

    user_input = message.text

    if user_input.startswith("@"):
        username = user_input[1:]
        user_data = db.find({"username": username})
    elif user_input.isdigit():
        user_id = int(user_input)
        user_data = db.find({"user_id": user_id})
    else:
        first_name = user_input
        user_data = db.find({"first_name": first_name})

    user_list = list(user_data)

    if len(user_list) > 0:
        user = user_list[0]
        await message.answer(search_user_mes(user), reply_markup=user_inline(user["user_id"]), parse_mode=None)
    else:
        await message.answer("Пользователь не найден\. Пожалуйста, попробуйте снова\.")

    await state.clear()

@router.message(StateFilter(Wait.waiting_support), IsAdmin())
async def search_support_handler(message: Message, state: FSMContext, bot: Bot):
    db = bot.db
    db.use_collection("support")

    support_id = message.text
    support_data = db.find({"id": support_id})
    support_list = list(support_data)

    print(support_data, support_list)
    if len(support_list) > 0:
        support = support_list[0]
        await message.answer(search_support_mes(support), parse_mode=None)
    else:
        await message.answer("Поддержка не найдена\. Пожалуйста, попробуйте снова\.")

    await state.clear()

@router.message(F.text == "📊 Статистика", IsAdmin())
async def stats_handler(message: Message, bot: Bot):

    msg = await message.answer("Собираю информацию\.\.\. Ждите\.")

    db = bot.db 
    db.use_collection("users")
    
    stats_data = db.find({"user_id": "stats"})
    stats_list = list(stats_data)

    operators_data = db.find({"level": 4})
    operators_list = list(operators_data)

    await msg.delete()
    await stats_message(stats_list, operators_list, message)

async def stats_message(stats, operators, message):
    if len(stats) > 0:
        stats_data = stats[0]
    else:
        await message.answer("Ошибка: статистика не найдена\.")
        return
    
    stats_message = f"""📊 *Статистика*: 
➖➖➖➖➖➖➖➖➖
⭐ *Всего отзывов*: {stats_data.get("all_rate", 0)}
👍 *Положительных отзывов*: {stats_data.get("plus_rate", 0)}
👎 *Отрицательных отзывов*: {stats_data.get("minus_rate", 0)}

☀ *Всего запросов за день*: {stats_data.get("all_supports_day", 0)}
📆 *Всего запросов за месяц*: {stats_data.get("all_supports_mouth", 0)}
📅 *Всего запросов*: {stats_data.get("all_supports", 0)}

👥 *Пользователей в системе*: {stats_data.get("users", 0)}
➖➖➖➖➖➖➖➖➖"""

    await message.answer(stats_message)

    for operator in operators:
        operator_message = f"""🎧 Оператор : 
        ➖➖➖➖➖➖➖➖➖
👤 Оператор: {operator.get("first_name", "Неизвестно")} (@{operator.get("username", "Неизвестно")})
🆔 Айди: {operator.get("user_id", "Неизвестно")}

⭐ Всего отзывов: {operator.get("all_rate", 0)}
👍 Положительных отзывов: {operator.get("plus_rate", 0)}
👎 Отрицательных отзывов: {operator.get("minus_rate", 0)}

☀ Запросов за день: {operator.get("supports_day", 0)}
📆 Запросов за месяц: {operator.get("supports_mouth", 0)}
📅 Всего запросов: {operator.get("all_supports", 0)}
    ➖➖➖➖➖➖➖➖➖"""
        
        await message.answer(operator_message, parse_mode=None)
