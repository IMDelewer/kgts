from aiogram.filters import Filter
from aiogram.types import Message

from data import Config

class IsAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in Config.admins