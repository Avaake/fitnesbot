from aiogram.filters import BaseFilter
from aiogram.types import Message

from typing import List


class IsAdmin(BaseFilter):
    """перевиряє чи є користувач адміном"""

    def __init__(self, user_id: int | List[int]) -> None:
        self.user_id = user_id

    async def __call__(self, message: Message):
        if isinstance(self.user_id, int):
            return message.from_user.id == self.user_id
        return message.from_user.id in self.user_id
