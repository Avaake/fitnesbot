from aiogram import Dispatcher, Bot
from database.database import DatabaseManager


class BasicInitialisation:
    def __init__(self, bot: Bot, dp: Dispatcher, db_manager: DatabaseManager):
        self.bot = bot
        self.dp = dp
        self.db_manager = db_manager
