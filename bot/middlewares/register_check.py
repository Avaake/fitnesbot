from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Any, Callable, Dict, Awaitable
from database.database import DatabaseManager
from aiogram.types import TelegramObject
import logging


class RegisterCheckMiddleware(BaseMiddleware):
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        user = event.from_user

        if user:
            user_check = await self.db_manager.verify_the_user_through_middleware(user.id)
            if int(user_check[0]) == 0:
                await self.db_manager.add_the_user_through_middleware(
                    user.id, user.first_name, user.username, user.language_code
                )
                await event.answer(text="Привіт я FintesBot допоможу тобі с тренуваннями")
            elif int(user_check[0]) == 1:
                await self.db_manager.update_last_date_the_user_through_middleware(user.id)
                logging.info(f"update last_date in user_id: {user.id}")
        return await handler(event, data)
