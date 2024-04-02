import pytest
from unittest.mock import AsyncMock

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from fitnesbot.handlers.my_account import MyAccount
from fitnesbot.keybords.fabrics import inline_builder_sql
from fitnesbot.keybords.inline import my_account_menu
from tests.utils import TEST_USER, TEST_CHAT


@pytest.mark.asyncio
async def test_my_account_cmd(bot, dispatcher, db_manager):
    my_account = MyAccount(bot=bot, dp=dispatcher,db_manager=db_manager)
    call = AsyncMock()
    await my_account.my_account_cmd(call)

    call.message.edit_text.assert_called_with("Це твій особистий кабінет", reply_markup=my_account_menu)


@pytest.mark.asyncio
async def test_my_training_account(bot, dispatcher, db_manager, memory_storage):
    my_account = MyAccount(bot=bot, dp=dispatcher, db_manager=db_manager)
    call = AsyncMock()

    await my_account.my_training_account(call=call)
    button_list = [("Створити тренування", "create_training")]
    call.message.edit_text.assert_called_with(text="Так як у вас не має тренування ви можете його створити, "
                                                   "але тренування може біти лише одне на акаунт, "
                                                   "щоб створити інше потрібно спочатку видалити існуюче",
                                              reply_markup=inline_builder_sql(button_list, sizes=1,
                                                                              add_cb="my_account"))
