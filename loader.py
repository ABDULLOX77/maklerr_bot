from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api.home_db import DatabaseHome
from utils.db_api.region_db import DatabaseRegion

from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
homes_db = DatabaseHome(path_to_db="data/homes.db")
region_db = DatabaseRegion(path_to_db="data/region.db")
