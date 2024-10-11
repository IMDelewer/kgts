from aiogram import Router, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards import rate_inline
from routers.support import Wait

router = Router()

@router.callback_query()
async def callback_handler(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = callback.data.split("|")
    action, id = data[0], int(data[1])

    db = bot.db  # Подразумеваем, что db — это объект класса Database

    rate_stars = {
        "one_star": "⭐",
        "two_stars": "⭐⭐",
        "three_stars": "⭐⭐⭐",
        "four_stars": "⭐⭐⭐⭐",
        "five_stars": "⭐⭐⭐⭐⭐"
    }

    match action:
        case "up_user":
            db.use_collection("users")
            
            # Используем метод update для частичного обновления документа
            result = db.update(
                {"user_id": id},  # Условие поиска документа
                {
                    "level": 4, 
                    "all_rate": 0, 
                    "plus_rate": 0, 
                    "minus_rate": 0, 
                    "supports_day": 0, 
                    "supports_month": 0, 
                    "all_supports": 0
                }
            )
            
            if result > 0:
                await callback.answer("Уровень пользователя повышен до оператора")
            else:
                await callback.answer("Ошибка: не удалось обновить пользователя")



        case "accept_rules":
            db.use_collection("users")
            db.update({"user_id": id}, {"level": 2})
            await callback.answer("Вы приняли правила! Пропишите /start")

        case "reject":
            db.use_collection("supports")
            support_data = db.find({"id": id})
            support_list = list(support_data)  # Преобразуем Cursor в список

            if support_list:
                support = support_list[0]

                if support.get("operid") == 0 and support.get("cancels", 0) < 4:
                    if callback.from_user.id not in support.get("cancel_ids", []):
                        # Увеличиваем число отказов и добавляем пользователя в cancel_ids
                        db.update({"id": id}, {"$inc": {"cancels": 1}, "$push": {"cancel_ids": callback.from_user.id}})
                        await callback.answer("Запрос отклонен.")
                    else:
                        await callback.answer("Похоже, вы уже отклонили этот запрос.")
                else:
                    await callback.answer("Вы не можете отклонить этот запрос." if support.get("cancels", 0) < 4 else "Похоже, этот запрос уже приняли.")
            else:
                await callback.answer("Запрос не найден.")

        case "accept":
            db.use_collection("supports")
            support_data = db.find({"id": id})
            support_list = list(support_data)  # Преобразуем Cursor в список

            if support_list:
                support = support_list[0]

                if support.get("operid", 0) == 0:
                    db.update({"id": id}, {"operid": callback.from_user.id, "status": "accepted"})

                    db.use_collection("users")
                    user_support_data = db.find({"user_id": callback.from_user.id})
                    user_support_list = list(user_support_data)  # Преобразуем Cursor в список

                    if user_support_list:
                        user_support = user_support_list[0]
                        db.update({"user_id": callback.from_user.id},
                            {
                                "current_support": id,
                                "supports_day": user_support.get("supports_day", 0) + 1,
                                "supports_month": user_support.get("supports_month", 0) + 1,
                                "all_supports": user_support.get("all_supports", 0) + 1
                            }
                        )
                        await send_message_to_user(bot, support.get("userid"), "Ваш запрос был принят\!")
                        await callback.answer("Напишите ваш ответ на вопрос.")
                        await state.set_state(Wait.waiting_message_support)
                else:
                    await callback.answer("Похоже, этот запрос уже приняли.")
            else:
                await callback.answer("Запрос не найден.")

        case "accept_answer":
            db.use_collection("users")
            user_data = db.find({"user_id": callback.from_user.id})
            user_list = list(user_data)

            if user_list:
                user = user_list[0]
                current_support = user.get("current_support", None)
                if current_support:
                    await send_message_to_user(
                        bot,
                        callback.from_user.id, 
                        """⭐ Оцените оператора
    ➖➖➖➖➖➖➖➖
    Поставьте оценку ниже\!
    Слева направо, от 1 до 5
    ➖➖➖➖➖➖➖➖
    """,
                        reply_markup=rate_inline(current_support)
                    )
                    db.update({"user_id": callback.from_user.id}, {"current_support": 0})

        case "rejest_answer":
            db.use_collection("users")
            db.update({"user_id": callback.from_user.id}, {"current_support": 0})
            await callback.answer("❌ Ответ не получен. Если ответ не получен, обратитесь в поддержку ещё раз.")

        case rate_action if rate_action in ["one_star", "two_stars", "three_stars", "four_stars", "five_stars"]:
            db.use_collection("users")
            stats_data = db.find({"user_id": "stats"})
            stats_list = list(stats_data)

            if stats_list:
                db.update({"user_id": "stats"}, {
                    "all_rate": stats_list[0].get("all_rate", 0) + 1,
                    f"{'plus_rate' if rate_action in ['three_stars', 'four_stars', 'five_stars'] else 'minus_rate'}": stats_list[0].get(('plus_rate' if rate_action in ['three_stars', 'four_stars', 'five_stars'] else 'minus_rate'), 0) + 1
                })

            db.use_collection("supports")
            support_data = db.find({"id": id})
            support_list = list(support_data)

            if support_list:
                support = support_list[0]
                db.update({"user_id": support["operid"]}, {
                    "all_rate": support.get("all_rate", 0) + 1,
                    f"{'plus_rate' if rate_action in ['three_stars', 'four_stars', 'five_stars'] else 'minus_rate'}": support.get(('plus_rate' if rate_action in ['three_stars', 'four_stars', 'five_stars'] else 'minus_rate'), 0) + 1
                })
            
            await callback.answer("Спасибо за отзыв!")

            await send_admin(callback, bot, rate_stars.get(action))

async def send_message_to_user(bot, user_id, text, reply_markup=None, parse_mode="MarkdownV2"):
    await bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup, parse_mode=parse_mode)

async def send_admin(callback, bot, rate):
    db = bot.db
    db.use_collection("users")
    
    for admin in bot.config.admins:
        await send_message_to_user(
            bot,
            admin,
            f"""✨ Новый отзыв на {rate} от {callback.from_user.first_name} \(@{callback.from_user.username}\)""",
            parse_mode=None
        )
