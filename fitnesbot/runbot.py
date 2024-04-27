from fastapi import FastAPI
from fastapi.applications import AppType

from fitnesbot.handlers import user_command, products, nutrition, my_account
from fitnesbot.callback_handlers import (pagination, spotting_exercises_call,
                                         sport_food_supplements_list,
                                         training_from_athletes, training_at_home, my_activity_tracker)
from fitnesbot.mini_app import mini_apps_handlers
from aiogram.fsm.storage.memory import MemoryStorage
from config import settings
from fitnesbot.middlewares.register_check import RegisterCheckMiddleware
from fitnesbot.utils.basemodel import BasicInitialisationBot

storage = MemoryStorage()


class RunBot(BasicInitialisationBot):
    def __init__(self):
        self.user_command = user_command.User()
        self.products = products.AddProducts()
        self.food_count = nutrition.Nutrition()
        self.pag = pagination.Pagin()
        self.train_call = spotting_exercises_call.SpottingExercises()
        self.sport_food_supplements_list = sport_food_supplements_list.SupplementsMenu()
        self.mini_apps_handlers = mini_apps_handlers.TelegramMiniAppsHandlers()
        self.training_from_athletes = training_from_athletes.TrainingFromAthletes()
        self.training_at_home = training_at_home.TrainingAtHome()
        self.my_account = my_account.MyAccount()
        self.my_workout_time = my_activity_tracker.MyActivityTracker()

    async def lifespan(self, app: FastAPI) -> AppType:
        try:
            await self.bot.set_webhook(url=f"{settings.webhook_url}/webhook",
                                       allowed_updates=self.dp.resolve_used_update_types(),
                                       drop_pending_updates=True)
            await self.db_manager.connect_db()
            await self.user_command.run()
            await self.products.run()
            await self.food_count.run()
            await self.pag.run()
            await self.train_call.run()
            await self.sport_food_supplements_list.run()
            await self.mini_apps_handlers.run()
            await self.training_from_athletes.run()
            await self.training_at_home.run()
            await self.my_account.run()
            await self.my_workout_time.run()

            self.dp.message.middleware(RegisterCheckMiddleware(self.db_manager))
            yield
            await self.bot.delete_webhook(drop_pending_updates=True)
        finally:
            await self.db_manager.disconnect_db()
