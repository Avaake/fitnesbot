from aiogram import F
from aiogram.types import CallbackQuery

from fitnesbot.keybords.fabrics import paginator_food, pagination_to_view_recipes_kb
from fitnesbot.keybords.inline import nutrition_menu, category_food
from fitnesbot.utils.func import CALL_FOOD_DICT

from fitnesbot.utils.basemodel import BasicInitialisationBot


class Nutrition(BasicInitialisationBot):
    async def nutrition_handler(self, call: CallbackQuery):
        await call.message.edit_text(text="Тут зможешь отримати інформацію стосовно харчування",
                                     reply_markup=nutrition_menu)
        await call.answer()

    async def cmd_food_list(self, call: CallbackQuery):
        await call.message.edit_text(f'Привіт! <b>{call.from_user.first_name}</b> це категорії продуктів.\nОбирай '
                                     f'категорію і ти побачиш назву, калорійність та БЖУ',
                                     reply_markup=category_food)
        await call.answer()

    async def call_fruit_dried_fruit_berrie(self, call: CallbackQuery):  # не работает food_information
        info_food = await self.db_manager.food_information(CALL_FOOD_DICT[call.data])

        await call.message.edit_text(
            f'page=0\n<b>Назва: </b>{info_food[0][0]}\n<b>Калорисность: </b>{info_food[0][1]}\n'
            f'<b>Билки: </b>{info_food[0][2]}\n<b>Жири: </b>{info_food[0][3]}\n'
            f'<b>Угливоди: </b>{info_food[0][4]}',
            reply_markup=paginator_food())
        await call.answer()

    async def recipes_info_handler(self, call: CallbackQuery):
        response = await self.db_manager.recipes_information()
        await call.message.edit_text(text=f'<b>Назва<a href="{response[0][1]}">:</a></b> {response[0][2]}'
                                          f'<b>Інгредієнти</b> {response[0][3]}',
                                     reply_markup=pagination_to_view_recipes_kb())
        await call.answer()

    async def run(self):
        self.dp.callback_query.register(self.nutrition_handler, F.data == "nutrition_call")
        self.dp.callback_query.register(self.cmd_food_list, F.data == "food_list")
        self.dp.callback_query.register(self.call_fruit_dried_fruit_berrie, F.data.in_(
            ["fruit_dried_fruit_berrie", "herb_vegetable", "mushroom_legume", "egg",
             "fish_seafood", "meat_offal_poultry", "sausage_product_canned_meat", "dairy_product",
             "flour_product_cereal", "nut", "confectionery_sweet", "fat_margarine_oil"]))
        self.dp.callback_query.register(self.recipes_info_handler, F.data == "recipes_call")
