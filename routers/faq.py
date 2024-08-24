from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
import pandas as pd
from fuzzywuzzy import process

def load_excel():
    df = pd.read_excel('data/faq.xlsx', sheet_name='Лист1', header=None)
    return df

def find_similar_text(df, search_text):
    if df.shape[1] < 2:
        raise ValueError("DataFrame должен содержать как минимум два столбца.")

    df.columns = ['A', 'B']

    choices = df['A'].tolist()
    best_match, score = process.extractOne(search_text, choices)

    if score > 85:
        matching_row = df[df['A'] == best_match]
        return matching_row['B'].values[0]
    else:
        return "Нечего не найдено. Попробуйте перефразировать текст"
    

router = Router()

class Answer(StatesGroup):
    waiting_message = State()

    
@router.message(F.text == "❓ FAQ")
async def faq_message(message: Message, state: FSMContext):
    faq = """❓ FAQ
➖➖➖➖➖➖➖➖➖
Задайте ваш вопрос ❓.
Я поищу его в моей базе 🔍.
➖➖➖➖➖➖➖➖➖
"""
    await message.answer(faq)
    await state.set_state(Answer.waiting_message)
    
@router.message(StateFilter(Answer.waiting_message))
async def faq_handler(message: Message, state: FSMContext):
    
    df = load_excel()
    result = find_similar_text(df, message.text)
    
    faq_answer = f"""✔ Ответ
➖➖➖➖➖➖➖➖➖
{result}
➖➖➖➖➖➖➖➖➖
"""
    
    await message.answer(faq_answer, disable_web_page_preview=True)
    
    await state.clear()