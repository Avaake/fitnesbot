import asyncio
import logging
from aiogram import Dispatcher, Bot
from fitnesbot.handlers import user_command, products, foodcount, my_account
from database.database import DatabaseManager
from fitnesbot.callbacks import (pagination, callback_food_list, spotting_exercises_call, sport_food_supplements_list,
                                 training_from_athletes, training_at_home)
from fitnesbot.mini_app import mini_apps_handlers
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aioredis import Redis
from config import settings
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from fitnesbot.middlewares.register_check import RegisterCheckMiddleware

# redis = Redis()
storage = MemoryStorage()


class RunBot:

    def __init__(self):
        self.bot = Bot(token=settings.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        self.dp = Dispatcher(storage=storage)  # RedisStorage(redis=redis)
        self.db_manager = DatabaseManager()

        self.user_command = user_command.User(bot=self.bot, dp=self.dp, db_manager=self.db_manager)
        self.products = products.AddProducts(bot=self.bot, dp=self.dp, db_manager=self.db_manager)
        self.food_count = foodcount.AddFood(bot=self.bot, dp=self.dp, db_manager=self.db_manager)
        self.pag = pagination.Pagin(bot=self.bot, dp=self.dp, db_manager=self.db_manager)
        self.call_food_list = callback_food_list.CallbackFoodList(bot=self.bot, dp=self.dp, db_manager=self.db_manager)
        self.train_call = spotting_exercises_call.SpottingExercises(bot=self.bot, dp=self.dp,
                                                                    db_manager=self.db_manager)
        self.sport_food_supplements_list = sport_food_supplements_list.SupplementsMenu(bot=self.bot, dp=self.dp,
                                                                                       db_manager=self.db_manager)
        self.mini_apps_handlers = mini_apps_handlers.TelegramMiniAppsHandlers(bot=self.bot, dp=self.dp,
                                                                              db_manager=self.db_manager)
        self.training_from_athletes = training_from_athletes.TrainingFromAthletes(bot=self.bot, dp=self.dp,
                                                                                  db_manager=self.db_manager)
        self.training_at_home = training_at_home.TrainingAtHome(bot=self.bot, dp=self.dp, db_manager=self.db_manager)
        self.my_account = my_account.MyAccount(bot=self.bot, dp=self.dp, db_manager=self.db_manager)

    async def main(self):
        try:
            await self.db_manager.connect_db()
            self.user_command.run()
            self.products.run()
            self.food_count.run()
            self.pag.run()
            self.call_food_list.run()
            self.train_call.run()
            self.sport_food_supplements_list.run()
            self.mini_apps_handlers.run()
            self.training_from_athletes.run()
            self.training_at_home.run()
            self.my_account.run()

            self.dp.message.middleware(RegisterCheckMiddleware(self.db_manager))
            # self.dp.callback_query.middleware(RegisterCheckMiddleware(self.db_manager))
            await self.bot.delete_webhook(drop_pending_updates=True)
            await self.dp.start_polling(self.bot)
        finally:
            await self.db_manager.disconnect_db()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                               ' - (Line: %(lineno)d [%(filename)s - %(funcName)s])')
    try:
        start_bot = RunBot()
        asyncio.run(start_bot.main())
    except KeyboardInterrupt:
        print('Exit')
