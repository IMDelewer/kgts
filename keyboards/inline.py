from aiogram.utils.keyboard import InlineKeyboardBuilder

def category_inline():
    builder = InlineKeyboardBuilder()

    builder.button(text="Brawl Stars", callback_data="brawlstars")

def profile_inline():
    builder = InlineKeyboardBuilder()

    builder.button(text="👥 Рефералка", callback_data="referals")
    builder.button(text="💸 Покупки", callback_data="buys")

    builder.adjust(2)
    return builder.as_markup()