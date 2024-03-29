from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from bot.utils.func import f
from typing import List


class Pagination(CallbackData, prefix="pag"):
    action: str
    page: int


class PaginationFood(CallbackData, prefix="pagfood"):
    action: str
    page: int


class Paginationmuscle(CallbackData, prefix="pagmuscle"):
    action: str
    page: int


class Paginationmuscleatlets(CallbackData, prefix="pagmuscleatl"):
    action: str
    page: int


class PaginationTrainingAtHome(CallbackData, prefix="pagtrainingathome"):
    action: str
    page: int


class PaginationMySportsExercisesInTraining(CallbackData, prefix="pagmysportsexercisesintraining"):
    action: str
    page: int



def paginator(page: int = 0):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='⬅', callback_data=Pagination(action='preliminary', page=page).pack()),
        InlineKeyboardButton(text='➡', callback_data=Pagination(action='next', page=page).pack()),
        width=2
    )

    return builder.as_markup()


def paginator_food(page: int = 0):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='⬅', callback_data=PaginationFood(action='preliminary_f', page=page).pack()),
        InlineKeyboardButton(text='➡', callback_data=PaginationFood(action='next_f', page=page).pack()),
        width=2
    ).row(InlineKeyboardButton(text="Назад", callback_data='food_list'))
    return builder.as_markup()


def paginator_muscle_worcout(page: int = 0):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='⬅', callback_data=Paginationmuscle(action='preliminary_m', page=page).pack()),
        InlineKeyboardButton(text="Назад", callback_data="fitness_menu"),
        InlineKeyboardButton(text='➡', callback_data=Paginationmuscle(action='next_m', page=page).pack()),
    )
    return builder.as_markup()


def paginator_muscle(link: str, page: int = 0):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='⬅', callback_data=Paginationmuscleatlets(action='preliminary_ma', page=page).pack()),
        InlineKeyboardButton(text='Відео с вправою', url=link),
        InlineKeyboardButton(text='➡', callback_data=Paginationmuscleatlets(action='next_ma', page=page).pack()),
    )
    return builder.as_markup()


def paginator_training_at_home(backwards: str, page: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='⬅',
                             callback_data=PaginationTrainingAtHome(action='preliminary_triathome', page=page).pack()),
        InlineKeyboardButton(text="Назад", callback_data=backwards),
        InlineKeyboardButton(text='➡',
                             callback_data=PaginationTrainingAtHome(action='next_triathome', page=page).pack()),
    )
    return builder.as_markup()


def pagination_my_sports_exercises_in_training_kb(page: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Додати до тренування", callback_data="add_to_your_workout")
    )
    builder.row(
        InlineKeyboardButton(text='⬅',
                             callback_data=PaginationMySportsExercisesInTraining(action="preliminary_mseit",
                                                                                 page=page).pack()),
        InlineKeyboardButton(text="Вибір іншого", callback_data="create_training"),
        InlineKeyboardButton(text='➡',
                             callback_data=PaginationMySportsExercisesInTraining(action="next_mseit",
                                                                                 page=page).pack())
    )
    builder.row(InlineKeyboardButton(text="Кабінет користувача", callback_data="my_account"))
    return builder.as_markup()


def build_inline_keyboard_sql(buttons: list):
    # call_buttons = [{'text': ''.join(buttons[i]), 'callback_data': f(str(buttons[i]))} for i in range(len(buttons))]
    call_buttons = []
    for i in range(len(buttons)):
        b = {'text': str(buttons[i][0]), 'callback_data': str(buttons[i][-1])}
        print(b)
        call_buttons.append(b)
    builder = InlineKeyboardBuilder()
    for button in call_buttons:
        builder.row(InlineKeyboardButton(text=button['text'], callback_data=button['callback_data']))
    return builder.as_markup()


def build_inline_keyboard(buttons: list, add_cb: str = None):
    call_buttons = [{'text': ''.join(buttons[i]), 'callback_data': f(str(buttons[i]))} for i in range(len(buttons))]
    # print(call_buttons)
    builder = InlineKeyboardBuilder()
    for button in call_buttons:
        # print(button)
        builder.row(InlineKeyboardButton(text=button['text'], callback_data=button['callback_data']))
    if add_cb is not None:
        builder.row(InlineKeyboardButton(text="Назад", callback_data=add_cb))
    return builder.as_markup()


# def inline_builder(text: str | List[str],
#                    callback_data: str | List[str],
#                    sizes: int | List[int] = 2, **kwargs) -> InlineKeyboardMarkup:
#     builder = InlineKeyboardBuilder()
#     if isinstance(text, str):
#         text = [text]
#     if isinstance(callback_data, str):
#         callback_data = [callback_data]
#     if isinstance(sizes, int):
#         sizes = [sizes]
#
#     [
#         builder.button(text=txt, callback_data=cb)
#         for txt, cb in zip(text, callback_data)
#     ]
#     builder.adjust(*sizes)
#     return builder.as_markup(**kwargs)


def inline_builder_sql(buttons: List[tuple],
                       sizes: int | List[int] = 2,
                       add_txt: str = "Назад",
                       add_cb: str = None,
                       call_url: str = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for text, callback_data in buttons:
        builder.button(text=text, callback_data=callback_data)

    builder.adjust(sizes)
    if call_url is not None:
        builder.row(InlineKeyboardButton(text="Купуйте перевірене", url=call_url))
    if add_cb is not None:
        builder.row(InlineKeyboardButton(text=add_txt, callback_data=add_cb))
    return builder.as_markup()


def inline_back_button(title: str, callback_title: str, call_url: str = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if call_url is not None:
        builder.add(InlineKeyboardButton(text="Купуйте перевірене", url=call_url))
    builder.row(InlineKeyboardButton(text=title, callback_data=callback_title))
    return builder.as_markup()
