from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "❓ FAQ")
async def faq_message(message: Message):
    faq = """❓ FAQ
➖➖➖➖➖➖➖➖➖
Задайте ваш вопрос ❓.
Я поищу его в моей базе 🔍.
➖➖➖➖➖➖➖➖➖
"""
    await message.answer(faq)