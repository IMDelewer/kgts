from aiogram import Bot, Dispatcher
from aiogram.types import Update

from data import *
from database.database import Database, User, Support

class DelBot(Bot):
    def __init__(
        self, 
        config : Config, 
        logger : Logger, 
        dp : Dispatcher,
        database: Database,
        user : User,
        support : Support,
        **kwargs
        ):

        self.config = config
        self.logger = logger
        self.dp = dp
        self.db = database
        self.user = user
        self.support = support

        super().__init__(self.config.token, **kwargs)
    
    async def on_startup(self):
        self.logger.start(f"Bot Started! Version : {self.config.version}")
        me = await self.get_me()
        self.logger.info(f"Bot name : {me.username} Created by delewer")

    
    async def on_shutdown(self):
        self.logger.close("Bye-Bye!")

    async def on_error(self, update: Update, exception: Exception):
        self.logger.error(f"Unexpected error: {exception}")

        return True