"""
Файл для створення бота
A file for creating a bot
"""
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import config as cfg

storage = MemoryStorage()
bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(storage=storage)
