from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from config import settings

def f(text: int | list):
    builder = ReplyKeyboardBuilder()

    if isinstance(text, str):
        text = [text]
    [builder.button(text=txt) for txt in text]
    # for button in text:
    #     builder.row(KeyboardButton(text=button))
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True, selective=True)
    # builder = InlineKeyboardBuilder()
    # for button in call_buttons:
    #     builder.row(InlineKeyboardButton(text=button['text'], callback_data=button['callback_data']))
    # return builder.as_markup()


meals_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Сніданок'),
            KeyboardButton(text='Обід')
        ],
        [
            KeyboardButton(text='Вечеря'),
            KeyboardButton(text='Перекус')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите дайствие из меню",
    selective=True
)

muscles = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='грудь'),
            KeyboardButton(text='трицепс'),
            KeyboardButton(text='спина')
        ],
        [
            KeyboardButton(text='бицепс'),
            KeyboardButton(text='ноги'),
            KeyboardButton(text='прес')

        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите дайствие из меню",
    selective=True
)

# main12 = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text='Вітамин А'),
#             KeyboardButton(text='Вітамин B'),
#             KeyboardButton(text='Вітамин C')
#         ],
#         [
#             KeyboardButton(text='Вітамин D'),
#             KeyboardButton(text='Вітамин E'),
#         ]
#     ],
#     resize_keyboard=True,
#     one_time_keyboard=True,
#     input_field_placeholder="Выберите",
#     selective=True
# )



webAppKeyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🧮 Калькулятор калорій та БЖВ", web_app=WebAppInfo(url=f"{settings.webhook_url}/calcbzy"))
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)

cancel_kb = ReplyKeyboardRemove()