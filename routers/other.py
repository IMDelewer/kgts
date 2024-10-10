from aiogram import Router, Bot, F
from aiogram.types import Message

router = Router()

@router.message(F.text == '💡 О роботе')
async def info_message(message: Message, bot: Bot):
    info = f"""💡 *О роботе*
➖➖➖➖➖➖➖➖
Это *оффициальный* бот поддержки созданный для *ОАО "КГТС"*
Писать по ошибкам: @imdelewer
Версия : *{bot.config.version}*
Этот бот [Open Source]({bot.config.github})
➖➖➖➖➖➖➖➖
"""
    await message.answer(info, disable_web_page_preview=True)