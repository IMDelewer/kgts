from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_button(builder, text, callback_data=None, url=None):
    """Вспомогательная функция для добавления кнопки в билдер."""
    if url:
        builder.button(text=text, url=url)
    else:
        builder.button(text=text, callback_data=callback_data)

def build_inline_keyboard(buttons, adjust_count=2):
    """Создание инлайн-клавиатуры с заданными кнопками."""
    builder = InlineKeyboardBuilder()
    for button in buttons:
        create_button(builder, **button)
    builder.adjust(adjust_count)
    return builder.as_markup(resize_keyboard=True)

def support_inline(user_id):
    buttons = [
        {"text": "✔ Принять", "callback_data": f"accept|{user_id}"},
        {"text": "❌ Отклонить", "callback_data": f"reject|{user_id}"}
    ]
    return build_inline_keyboard(buttons)

def subscribe_inline(arg):
    buttons = [
        {"text": "❤ Подписаться", "url": "https://t.me/OAOKGTS"},
        {"text": "✔ Проверить", "callback_data": f"check_sub|{arg}"}
    ]
    return build_inline_keyboard(buttons)

def user_inline(user_id):
    buttons = [
        {"text": "⬆ Повысить", "callback_data": f"up_user|{user_id}"}
    ]
    return build_inline_keyboard(buttons, adjust_count=1)

def rules_inline(arg):
    buttons = [
        {"text": "✔ Принять", "callback_data": f"accept_rules|{arg}"}
    ]
    return build_inline_keyboard(buttons, adjust_count=1)

def answer_inline(arg):
    buttons = [
        {"text": "✔ Ответ получен", "callback_data": f"accept_answer|{arg}"},
        {"text": "❌ Ответ не получен", "callback_data": f"rejest_answer|{arg}"}
    ]
    return build_inline_keyboard(buttons)

def rate_inline(arg):
    buttons = [
        {"text": "⭐", "callback_data": f"one_star|{arg}"},
        {"text": "⭐", "callback_data": f"two_stars|{arg}"},
        {"text": "⭐", "callback_data": f"three_stars|{arg}"},
        {"text": "⭐", "callback_data": f"four_stars|{arg}"},
        {"text": "⭐", "callback_data": f"five_stars|{arg}"}
    ]
    return build_inline_keyboard(buttons, adjust_count=5)
