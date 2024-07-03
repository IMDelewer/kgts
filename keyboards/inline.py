from aiogram.utils.keyboard import InlineKeyboardBuilder

def support_inline(id):
    builder = InlineKeyboardBuilder()

    builder.button(text="✔ Принят", callback_data=f"accept|{id}")
    builder.button(text="❌ Отклонить", callback_data=f"reject|{id}")

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)