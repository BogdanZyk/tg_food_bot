from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from config import tg_bot_token
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token = tg_bot_token)
dp = Dispatcher(bot, storage = storage)