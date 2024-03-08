from aiogram import F, Bot, Dispatcher
from aiogram.types import CallbackQuery
from database.database import DatabaseManager
from bot.keybords import fabrics, inline
from bot.utils.func import CALL_FOOD_DICT
from bot.utils.basemodel import BasicInitialisation


class CallbackFoodList(BasicInitialisation):
    def __init__(self, bot: Bot, dp: Dispatcher, db_manager: DatabaseManager):
        super().__init__(bot, dp, db_manager)

    async def cmd_food_list(self, call: CallbackQuery):
        await call.message.edit_text(f'Привіт! <b>{call.from_user.first_name}</b> це категорії продуктів.\nОбирай '
                                     f'категорію і ти побачиш назву, калорійність та БЖУ',
                                     reply_markup=inline.category_food)
        await call.answer()

    async def call_fruit_dried_fruit_berrie(self, call: CallbackQuery): # не работает food_information
        info_food = await self.db_manager.food_information(CALL_FOOD_DICT[call.data])

        await call.message.edit_text(
            f'page=0\n<b>Назва: </b>{info_food[0][0]}\n<b>Калорисность: </b>{info_food[0][1]}\n'
            f'<b>Билки: </b>{info_food[0][2]}\n<b>Жири: </b>{info_food[0][3]}\n'
            f'<b>Угливоди: </b>{info_food[0][4]}',
            reply_markup=fabrics.paginator_food())
        await call.answer()

    def run(self):
        self.dp.callback_query.register(self.cmd_food_list, F.data == "food_list")
        self.dp.callback_query.register(self.call_fruit_dried_fruit_berrie, F.data.in_(
            ["fruit_dried_fruit_berrie", "herb_vegetable", "mushroom_legume", "egg",
             "fish_seafood", "meat_offal_poultry", "sausage_product_canned_meat", "dairy_product",
             "flour_product_cereal", "nut", "confectionery_sweet", "fat_margarine_oil"]))
