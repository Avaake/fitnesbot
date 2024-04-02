import pytest
import asyncio
import pytest_asyncio
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from mocked_bot import MockedBot
from database.database import DatabaseManager


@pytest_asyncio.fixture(scope="session")
async def memory_storage():
    tmp_storage = MemoryStorage()
    try:
        yield tmp_storage
    finally:
        await tmp_storage.close()


@pytest.fixture()
def bot():
    return MockedBot()


@pytest_asyncio.fixture()
async def dispatcher():
    dp = Dispatcher()
    await dp.emit_startup()
    try:
        yield dp
    finally:
        await dp.emit_shutdown()


@pytest_asyncio.fixture()
async def db_manager():
    db_manager = DatabaseManager()
    try:
        await db_manager.connect_db()
        yield db_manager
    finally:
        await db_manager.disconnect_db()
