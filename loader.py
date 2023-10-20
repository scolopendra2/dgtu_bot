from data import config
from aiogram import Bot, Dispatcher, types

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
