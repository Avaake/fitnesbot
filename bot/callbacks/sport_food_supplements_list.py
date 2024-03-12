from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandObject
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message, CallbackQuery
from database.database import DatabaseManager
from bot.keybords import fabrics, builders
from bot.keybords.inline import menu
from bot.utils.states import AdditiveNamesCall
from bot.utils.basemodel import BasicInitialisation


class SupplementsMenu(BasicInitialisation):
    """
    Клас SupplementsMenu успадковується від класу BasicInitialisation
    містить обробники callbecks які повертають інформацію о спотривних/харчових добавках, вытамінах
    """

    def __init__(self, bot: Bot, dp: Dispatcher, db_manager: DatabaseManager):
        super().__init__(bot, dp, db_manager)

    async def additives_menu(self, call: CallbackQuery) -> None:
        res = await self.db_manager.additives_inline()
        print(res)
        await call.message.edit_text(text='<b>Виберай</b>',
                                     reply_markup=fabrics.inline_builder_sql(res, add_cb='start'))
        await call.answer()

    async def additives_groups(self, call: CallbackQuery) -> None:
        res = await self.db_manager.additives_groups_inline2(call.data)
        if len(res) == 0:
            res = await self.db_manager.additives_groups_inline(call.data)
            await call.message.edit_text(text=res[0][0],
                                         reply_markup=fabrics.inline_back_button(title="Назад",
                                                                                 callback_title="additives_call",
                                                                                 call_url=res[0][-1]))
        else:
            result = [(i[0], i[1]) for i in res]
            await call.message.edit_text(text=res[0][2],
                                         reply_markup=fabrics.inline_builder_sql(result, sizes=3,
                                                                                 add_cb="additives_call",
                                                                                 call_url=res[0][-1]))
        await call.answer()

    async def additives_subgroup(self, call: CallbackQuery) -> None:
        previous_title_and_txt = await self.db_manager.callback_for_additives_subgroup(call.data)
        await call.message.edit_text(
            text=previous_title_and_txt[-1],
            reply_markup=fabrics.inline_back_button(
                title="Назад", callback_title=previous_title_and_txt[0]))
        await call.answer()

    def run(self):
        self.dp.callback_query.register(self.additives_menu, F.data == "additives_call")
        self.dp.callback_query.register(self.additives_groups, F.data.in_(
            ["additive_group_1", "additive_group_2", "additive_group_3", "additive_group_4",
             "additive_group_5", "additive_group_6", "additive_group_7", "additive_group_8",
             "additive_group_9", "additive_group_10"]))
        self.dp.callback_query.register(self.additives_subgroup, F.data.in_(
            ["vitaminA", "vitaminB", "vitaminD", "vitaminC", "vitaminE", "LCarnitine", "Thermal_incinerators",
             "Glucosamine", "Chondroitin", "Cols_sup_joint", "BCAA", "EAA", "Arginine", "Glutamine",
             "Magnesium", "Calcium", "Iron", "Zinc", "Prewor_stimul", "Nit_oxid_addi", "HMB", "Ster_repl", "Caffeine",
             "Beta_alanine", "DAA", "Omega3", "Omega6", "Omega9"]))
