from aiogram import Dispatcher, Bot

from config import settings
from data.database import DatabaseManager
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aioredis import Redis
from aiogram.fsm.storage.redis import RedisStorage

redis = Redis()

# storage = MemoryStorage()

storage = RedisStorage(redis=redis)


class BasicInitialisationBot:

    bot = Bot(
        token=settings.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(
        storage=storage
    )  # RedisStorage(redis=redis) Dispatcher(storage=storage)
    db_manager = DatabaseManager()
