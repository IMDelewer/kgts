from aiogram.filters import Filter
from aiogram import types, Dispatcher

from data import Config

class IsAdmin(Filter):
    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id in Config.admins

class IsUser(Filter):
    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id not in Config.admins