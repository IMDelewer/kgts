from aiogram.utils.keyboard import ReplyKeyboardBuilder

def main_reply():
    builder = ReplyKeyboardBuilder()
    
    builder.button(text="🎧 Поддержка")
    builder.button(text="❓ FAQ")
    builder.button(text="💡 О роботе")

    builder.adjust(1, 3)
    return builder.as_markup(resize_keyboard=True)
