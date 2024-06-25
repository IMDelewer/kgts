import importlib
import os
from aiogram import Dispatcher

def setup_routers(dp: Dispatcher, logger):
    routers_path = os.path.join(os.path.dirname(__file__), '')
    for filename in os.listdir(routers_path):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = f'routers.{filename[:-3]}'  # Имя модуля без расширения .py
            module = importlib.import_module(module_name)
            if hasattr(module, 'router'):
                router = getattr(module, 'router')
                dp.include_router(router)
                logger.info(f"Router loaded: {module_name}")