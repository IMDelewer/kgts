from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

import pandas as pd
from fuzzywuzzy import process

router = Router()

class Answer(StatesGroup):
    waiting_message = State()

def load_excel():
    try:
        df = pd.read_excel('data/faq.xlsx', sheet_name='Лист1', header=None)
        if df.shape[1] < 2:
            raise ValueError("DataFrame должен содержать как минимум два столбца.")
        df.columns = ['A', 'B']
        return df
    except Exception as e:
        print(f"Ошибка при запуске файла : {e}")
        return None

faq_data = load_excel()

def find_similar_text(df, search_text):
    choices = df['A'].tolist()
    best_match, score = process.extractOne(search_text, choices)

    if score > 85:
        return df[df['A'] == best_match]['B'].values[0]
    return "Нечего не найдено. Попробуйте перефразировать текст."

@router.message(F.text == "❓ FAQ")
async def faq_message(message: Message, state: FSMContext):
    faq_intro = """*❓ FAQ*
➖➖➖➖➖➖➖➖➖
❓ Задайте ваш *вопрос*\.
🔍 Я поищу его в *моей базе*\.
➖➖➖➖➖➖➖➖➖"""
    
    await message.answer(faq_intro)
    await state.set_state(Answer.waiting_message)
    
@router.message(StateFilter(Answer.waiting_message))
async def faq_handler(message: Message, state: FSMContext):
    if faq_data is None:
        await message.answer("Произошла ошибка при загрузке данных. Пожалуйста, попробуйте позже.")
        await state.clear()
        return
    
    result = find_similar_text(faq_data, message.text)
    
    faq_answer = f"""✔ Ответ
➖➖➖➖➖➖➖➖➖
{result}
➖➖➖➖➖➖➖➖➖"""
    
    await message.answer(faq_answer, disable_web_page_preview=True, parse_mode=None)
    await state.clear()
