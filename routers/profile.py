from aiogram import Router, Bot, types, F

from keyboards import profile_inline

router = Router()

@router.message(F.text == '👤 Профиль')
async def profile(message: types.Message, bot: Bot):
    database = bot.db
    database.use_collection("users")

    helper = bot.help
    user = database.find({"userid": message.from_user.id})
    
    profile_message = f"""
    👤 Профиль
➖➖➖➖➖➖➖➖➖➖➖
Юзернейм : {user["username"]}
Айди : {user["userid"]}
Уровень : {helper.get_status(user["level"])}
Рефералок : {user["refs"]}
Покупок : {user["buys"]}
➖➖➖➖➖➖➖➖➖➖➖
    """

    await message.answer(profile_message, reply_markup=profile_inline())

@router.callback_query()
async def profile_callback(callback_query: types.CallbackQuery):
    if callback_query == "referals":
        await callback_query.answer("asdas")