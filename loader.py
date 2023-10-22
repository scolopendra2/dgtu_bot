from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

engine = create_engine(
    f'postgresql+psycopg2://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@'
    f'{config.POSTGRES_HOST}:{5432}/{config.POSTGRES_DB}'
)

local_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)

db = local_session()

Base = declarative_base()
