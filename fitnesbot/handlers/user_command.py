from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove, Message, CallbackQuery
from fitnesbot.keybords.inline import menu, help_menu
from fitnesbot.keybords.fabrics import inline_back_button
from fitnesbot.utils.basemodel import BasicInitialisationBot
from fitnesbot.utils.states import LetterToTechnicalSupport

class User(BasicInitialisationBot):
    """
        Клас User містить обробники команд які доступні всім користувачас
    """

    async def cmd_start(self, message: Message):
        """Обробник команди start"""
        await message.answer(f'Hello {message.from_user.first_name}', reply_markup=menu)

    async def call_cmd_start(self, call: CallbackQuery, state: FSMContext):
        """Обробник команди start"""
        await state.clear()
        await call.message.edit_text(f'Hello {call.message.from_user.first_name}', reply_markup=menu)

    async def call_help_handler(self, call: CallbackQuery):
        await call.message.edit_text(f'{call.message.from_user.first_name} тут ти зможешь отримати '
                                     f'інформацію стосовно функціоналу Fitness-бота', reply_markup=help_menu)

    async def information_about_the_functionality_fitnessbot(self, call: CallbackQuery):
        await call.message.edit_text(text="Інфо",
                                     reply_markup=inline_back_button(title="Головде меню", callback_title="start"))

    async def create_a_message_to_technical_support(self, call: CallbackQuery, state: FSMContext):
        await state.set_state(LetterToTechnicalSupport.letter_in_support)
        await call.message.edit_text(text="""Створюй та відправляй повідомлення до нас.
                            З повагою підтримка Fitnessbot""")

    async def send_a_message_to_technical_support(self, message: Message, state: FSMContext):
        await state.update_data(letter_in_support=message.text)
        data = await state.get_data()
        await self.bot.send_message(chat_id=821674004, text=data['letter_in_support'])
        del data['letter_in_support']
        await state.set_data(data)
        await message.answer("Повідомлення було надіслано .")
        return await self.cmd_start(message=message)

    async def cancel_handler(self, message: Message, state: FSMContext):
        """Обробник команди cancel зупиняє state"""
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.clear()
        await message.answer(
            "Cancelled.",
            reply_markup=ReplyKeyboardRemove(),
        )

    async def run(self):
        """регеєструє всі обробники """
        self.dp.message.register(self.cmd_start, Command('start'))
        self.dp.callback_query.register(self.call_cmd_start, F.data == 'start')
        self.dp.callback_query.register(self.call_help_handler, F.data == "help_call")
        self.dp.callback_query.register(self.information_about_the_functionality_fitnessbot,
                                        F.data == "get_information_help")
        self.dp.callback_query.register(self.create_a_message_to_technical_support,
                                        F.data == "letter_to_technical_support")
        self.dp.message.register(self.send_a_message_to_technical_support, LetterToTechnicalSupport.letter_in_support)
        self.dp.message.register(self.cancel_handler, Command("cancel"))

