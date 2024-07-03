from aiogram.filters import BaseFilter
from aiogram import types, Dispatcher

from data import Config

class IsAdmin(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id in Config.admins
