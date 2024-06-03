from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from config import settings


cancel_kb = ReplyKeyboardRemove()


def web_keyboard_builder(txt: str, webapp: str):
    builder = ReplyKeyboardBuilder()
    builder.button(text=txt, web_app=WebAppInfo(url=f"{settings.webhook_url}{webapp}"))
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True, selective=True)
