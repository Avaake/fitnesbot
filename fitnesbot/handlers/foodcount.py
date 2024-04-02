from aiogram import F, Dispatcher, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from fitnesbot.utils.states import FoodCounting
from database.database import DatabaseManager
from fitnesbot.keybords.builders import meals_kb
from fitnesbot.utils.basemodel import BasicInitialisation


class AddFood(BasicInitialisation):
    def __init__(self, bot: Bot, dp: Dispatcher, db_manager: DatabaseManager):
        super().__init__(bot, dp, db_manager)

    async def cmd_food(self, call: CallbackQuery, state: FSMContext):
        await state.set_state(FoodCounting.meal)
        await call.message.answer("Привіт. Вибери прийом їжі", reply_markup=meals_kb)
        await call.answer()

    async def load_meal(self, message: Message, state: FSMContext):
        await state.update_data(meal=message.text)
        await state.set_state(FoodCounting.food)
        await message.answer('Введіть назву їжі', reply_markup=ReplyKeyboardRemove())

    async def incorrect_load_meal(self, message: Message, state: FSMContext):
        await message.answer("Нажми на кнопку")

    async def load_food(self, message: Message, state: FSMContext):
        await state.update_data(food=message.text)
        data = await state.get_data()
        await state.clear()
        formatted_text = list(data.values())
        res = await self.db_manager.add_count_calories(formatted_text, message.from_user.username)
        print(res)
        await message.answer(f"<b>Прийом їжі:</b> {res[0]}\n"
                             f"<b>Продукти:</b> {res[1]}\n"
                             f"<b>Калорії:</b> {res[2]}\n"
                             f"<b>Білки:</b> {res[3]}\n"
                             f"<b>Жири:</b> {res[4]}\n"
                             f"<b>Вугливоди:</b> {res[5]}")

    def run(self):
        self.dp.callback_query.register(self.cmd_food, F.data == 'add_food')
        self.dp.message.register(self.load_meal, FoodCounting.meal,
                                 F.text.in_(["Сніданок", "Обід", "Вечеря", "Перекус"]))
        self.dp.message.register(self.incorrect_load_meal, FoodCounting.meal)
        self.dp.message.register(self.load_food, FoodCounting.food)
