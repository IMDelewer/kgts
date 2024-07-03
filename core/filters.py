from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter

from data import admins

class IsAdmin(BoundFilter):

    async def check(self, message: Message):
        return message.from_user.id in admins

def reg_filters(dp: Dispatcher):
    dp.filters_factory.bind(IsAdmin)