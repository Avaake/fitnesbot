import pytest
from unittest.mock import AsyncMock

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from fitnesbot.handlers.user_command import User
from fitnesbot.keybords.inline import menu
from tests.utils import TEST_USER, TEST_CHAT


@pytest.mark.asyncio
async def test_start_handler(bot, dispatcher, db_manager):
    user_command = User(bot=bot, dp=dispatcher, db_manager=db_manager)
    message = AsyncMock()
    await user_command.cmd_start(message)

    message.answer.assert_called_with(f'Hello {message.from_user.first_name}', reply_markup=menu)


@pytest.mark.asyncio
async def test_call_start_handler(memory_storage, bot, dispatcher, db_manager):
    user_command = User(bot=bot, dp=dispatcher, db_manager=db_manager)
    call = AsyncMock()
    state = FSMContext(
        storage=memory_storage,
        key=StorageKey(bot_id=bot.id, user_id=TEST_USER.id, chat_id=TEST_CHAT.id)
    )
    await user_command.call_cmd_start(call=call, state=state)

    assert await state.get_state() is None

    call.message.edit_text.assert_called_once()
    call.message.edit_text.assert_called_with(f'Hello {call.message.from_user.first_name}', reply_markup=menu)
