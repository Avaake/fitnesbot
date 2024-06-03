from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from fitnesbot.filters.is_admin import IsAdmin
from fitnesbot.utils.states import ProductFPC
from fitnesbot.utils.basemodel import BasicInitialisationBot

def isfloat(value):
    try:
        float(value)
        return True
    except:
        return False


class AddProducts(BasicInitialisationBot):
    """
        Врозробці тільки для адмінів
    """
    async def cmd_product(self, call: CallbackQuery, state: FSMContext):
        await state.set_state(ProductFPC.product_name)
        await call.message.answer("Давай почнемо, введи назву продукту")
        await call.answer()

    async def load_product_name(self, message: Message, state: FSMContext):
        await state.update_data(product_name=message.text)
        await state.set_state(ProductFPC.calorie_value)
        await message.answer("Введіть калорійність продукту на 100 грамів", )

    async def load_calorie_value(self, message: Message, state: FSMContext):
        if isfloat(message.text):
            await state.update_data(calorie_value=message.text)
            await state.set_state(ProductFPC.fats)
            await message.answer("Введіть кількість жирів на 100 грамів")
        else:
            await message.reply("Має містити ціле число або десятковий дріб")

    async def load_fats(self, message: Message, state: FSMContext):
        if isfloat(message.text):
            await state.update_data(fats=message.text)
            await state.set_state(ProductFPC.proteins)
            await message.answer("Введіть кількість білків на 100 грамів")
        else:
            await message.reply("Має містити ціле число або десятковий дріб")

    async def load_proteins(self, message: Message, state: FSMContext):
        if isfloat(message.text):
            await state.update_data(proteins=message.text)
            await state.set_state(ProductFPC.carbohydrates)
            await message.answer("Видите количество вуглеводів на 100 грамів")
        else:
            await message.reply("Має містити ціле число або десятковий дріб")

    async def load_carbohydrates(self, message: Message, state: FSMContext):
        if isfloat(message.text):
            await state.update_data(carbohydrates=message.text)
            data = await state.get_data()
            await state.clear()
            formatted_text = [float(value) if value.isdigit() or isfloat(value) else value for value in data.values()]
            # formatted_text = list(data.values())
            print(formatted_text)
            await self.db_manager.add_products(message.from_user.username, formatted_text)
            await message.answer(f"<b>Название:</b> {formatted_text[0]}\n"
                                 f"<b>Калорисность:</b> {formatted_text[1]}\n"
                                 f"<b>Жири:</b> {formatted_text[2]}\n"
                                 f"<b>Билки:</b> {formatted_text[3]}\n"
                                 f"<b>Угливоди:</b> {formatted_text[4]}\n")
        else:
            await message.answer("Має містити ціле число або десятковий дріб")

    async def run(self):
        self.dp.callback_query.register(self.cmd_product, F.data == "add_callback", IsAdmin(5600998025))
        self.dp.message.register(self.load_product_name, ProductFPC.product_name)
        self.dp.message.register(self.load_calorie_value, ProductFPC.calorie_value)
        self.dp.message.register(self.load_fats, ProductFPC.fats)
        self.dp.message.register(self.load_proteins, ProductFPC.proteins)
        self.dp.message.register(self.load_carbohydrates, ProductFPC.carbohydrates)
