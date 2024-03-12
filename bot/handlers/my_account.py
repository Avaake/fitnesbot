from bot.utils.basemodel import BasicInitialisation
from aiogram import Bot, Dispatcher, F
from database.database import DatabaseManager
from aiogram.types import CallbackQuery
from bot.keybords.inline import my_account_menu, playlists_menu


class MyAccount(BasicInitialisation):
    def __init__(self, bot: Bot, dp: Dispatcher, db_manager: DatabaseManager):
        super().__init__(bot, dp, db_manager)

    async def my_account_cmd(self, call: CallbackQuery):
        await call.message.edit_text("Це твій особистий кабінет", reply_markup=my_account_menu)
        await call.answer()

    async def playlists(self, call: CallbackQuery):
        await call.message.edit_text("Ось плейлисти Spotify для вашого тренування. Приємного прослуховування",
                                     reply_markup=playlists_menu)
        await call.answer()

    def run(self):
        self.dp.callback_query.register(self.my_account_cmd, F.data == "my_account")
        self.dp.callback_query.register(self.playlists, F.data == "Playlists")
