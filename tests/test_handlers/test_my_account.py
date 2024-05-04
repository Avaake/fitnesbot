import pytest
from unittest.mock import AsyncMock

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from fitnesbot.handlers.my_account import MyAccount
from fitnesbot.keybords import builders
from fitnesbot.keybords.fabrics import inline_builder_sql
from fitnesbot.keybords.inline import my_account_menu
from tests.utils import TEST_USER, TEST_CHAT

my_account = MyAccount()
rec_text = "Вимкнути рекомендації 🔕💡"
button_list = [("Створити тренування 🏋️‍♂️✏️", "create_training")]

@pytest.mark.asyncio
async def test_my_account_cmd():
    call = AsyncMock()
    await my_account.my_account_cmd(call)

    call.message.edit_text.assert_called_with(text=f"Привіт {call.from_user.first_name}! Це твій особистий кабінет. "
                                                   f"Можеш починати тичяти по кнопкам", reply_markup=my_account_menu)
    call.message.edit_text.assert_called_once()
@pytest.mark.asyncio
async def test_my_training_account(db_manager):
    call = AsyncMock()
    await my_account.my_training_account(call=call)
    call.message.edit_text.assert_called_with(text="Так як у вас не має тренування ви можете його створити, "
                                                   "але тренування може бути лише одне на акаунт, "
                                                   "щоб створити інше потрібно спочатку видалити існуюче",
                                              reply_markup=inline_builder_sql(button_list, sizes=1,
                                                                              back_cb="my_account",
                                                                              add_text=rec_text,
                                                                              add_cb="recommendations_for_the_disease"))
    call.message.edit_text.assert_called_once()


@pytest.mark.asyncio
async def test_create_my_workout(db_manager, memory_storage, bot):
    call = AsyncMock()
    recommendation_response = 1
    await my_account.updating_the_user_recommendation_index(call=call)

    call.answer.assert_called_with(
        "Рекомендації було увімкнуто" if recommendation_response == 0 else "Рекомендації було вимкнуто")
    call.message.edit_text.assert_called_once()

@pytest.mark.asyncio
async def test_delete_my_workout(db_manager, memory_storage, bot):
    call = AsyncMock()
    await my_account.delete_my_workout(call=call)

    call.answer.assert_called_with(text="Ваше тренування було видалено!!!")
    call.answer.assert_called_once()
