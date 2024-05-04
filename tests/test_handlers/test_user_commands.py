from datetime import datetime

import pytest
from unittest.mock import AsyncMock

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from fitnesbot.handlers.user_command import UserCommans
from fitnesbot.keybords.inline import menu, help_menu
from fitnesbot.utils.states import LetterToTechnicalSupport
from tests.utils import TEST_USER, TEST_CHAT
from aiogram.types import User, Chat, Message, CallbackQuery, Update

user_command = UserCommans()

@pytest.mark.asyncio
async def test_start_handler():
    message = AsyncMock()
    await user_command.cmd_start(message)
    message.answer.assert_called_with(f'Привіт {message.from_user.first_name}, це головне меню боту', reply_markup=menu)
    message.answer.assert_called_once()

@pytest.mark.asyncio
async def test_call_start_handler(memory_storage, bot):
    call = AsyncMock()
    state = FSMContext(
        storage=memory_storage,
        key=StorageKey(bot_id=bot.id, user_id=TEST_USER.id, chat_id=TEST_CHAT.id))
    await user_command.call_cmd_start(call=call, state=state)

    assert await state.get_state() is None
    call.message.edit_text.assert_called_with(f'Привіт {call.message.from_user.first_name}, це головне меню боту ',
                                              reply_markup=menu)
    call.message.edit_text.assert_called_once()

@pytest.mark.asyncio
async def test_call_help_handler():
    call = AsyncMock()
    await user_command.call_help_handler(call=call)
    call.message.edit_text.assert_called_with(f'{call.message.from_user.first_name} тут ти зможешь отримати '
                                              f'інформацію стосовно функціоналу Fitness-бота', reply_markup=help_menu)
    call.message.edit_text.assert_called_once()

@pytest.mark.asyncio
async def test_create_a_message_to_technical_support(memory_storage, bot):
    call = AsyncMock()
    state = FSMContext(
        storage=memory_storage,
        key=StorageKey(bot_id=bot.id, user_id=TEST_USER.id, chat_id=TEST_CHAT.id))
    await user_command.create_a_message_to_technical_support(call=call, state=state)
    assert await state.get_state() == 'LetterToTechnicalSupport:letter_in_support'
    call.message.edit_text.assert_called_with(text="""Створюй та відправляй повідомлення до нас.
                            З повагою підтримка Fitnessbot""")
    call.message.edit_text.assert_called_once()


from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_send_a_message_to_technical_support2(db_manager, memory_storage, bot):
    message_text = "Текст повідомлення до техпідтримки"
    # Створюємо мокові об'єкти
    message = AsyncMock()
    message.text = message_text
    state = FSMContext(
        storage=memory_storage,
        key=StorageKey(bot_id=bot.id, user_id=TEST_USER.id, chat_id=TEST_CHAT.id)
    )
    await state.set_state(LetterToTechnicalSupport.letter_in_support)
    # Оновлюємо дані перед викликом функції
    await state.update_data(letter_in_support=message_text)

    # Викликаємо метод
    await user_command.send_a_message_to_technical_support(message=message, state=state)

    # Перевіряємо, чи дані були встановлені в стані правильно
    data = await state.get_data()

    # Перевіряємо, чи було відправлено повідомлення з правильним текстом
    usend_message_admin.assert_called_with(chat_id=821674004, text=data['letter_in_support'])

