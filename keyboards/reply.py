from aiogram.utils.keyboard import ReplyKeyboardBuilder

def build_reply_keyboard(buttons, adjust_count):
    """Создание клавиатуры с заданными кнопками и настройками."""
    builder = ReplyKeyboardBuilder()
    for button in buttons:
        builder.button(text=button)
    builder.adjust(*adjust_count)
    return builder.as_markup(resize_keyboard=True)

def main_reply():
    buttons = ["🎧 Поддержка", "❓ FAQ", "💡 О роботе"]
    return build_reply_keyboard(buttons, adjust_count=(1, 3))

def admin_reply():
    buttons = ["🎧 Поддержка", "🔍 Поиск юзера", "🔍 Поиск поддержки", "📊 Статистика"]
    return build_reply_keyboard(buttons, adjust_count=(1, 2))
