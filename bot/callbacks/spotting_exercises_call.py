from aiogram import F, Bot, Dispatcher
from aiogram.types import CallbackQuery
from database.database import DatabaseManager
from bot.keybords import fabrics, inline
from bot.utils import func
from aiogram.fsm.context import FSMContext
from bot.utils.states import MuscleIDs
from bot.utils.basemodel import BasicInitialisation


# muscle = func.MuscleID


class SpottingExercises(BasicInitialisation):
    """Клас TrainingCall містить обробники з тренуванням"""

    def __init__(self, bot: Bot, dp: Dispatcher, db_manager: DatabaseManager):
        # self.user_data = {}  # Словник для збереження даних користувачів
        super().__init__(bot, dp, db_manager)

    async def cmd_workouts(self, call: CallbackQuery):
        """
            обробники відповідає на кнопку 'Тренування' та callback workouts
            та повертає Inline клавіатуру с тренуваннями
        """
        await call.message.edit_text(f'Обирай, що тобі потрібно та тицяй на кнопку',
                                     reply_markup=inline.training_menu)
        await call.answer()

    async def cmd_list_workout(self, call: CallbackQuery, state: FSMContext):
        """
            обробники відповідає на кнопку 'Фітнес-Меню' та callback fitness_menu
            та повертає Inline клавіатуру з завдани мязів
        """
        res = await self.db_manager.muscle_group_inline()
        # print(res)
        await state.set_state(MuscleIDs.muscle_id)
        await call.message.edit_text(f"<b>Виберіть групу м'язів, для якої ви хочете переглянути вправи</b>",
                                     reply_markup=fabrics.inline_builder_sql(res, sizes=3, add_cb='workouts'))
        await call.answer()

    async def cmd_muscle_name(self, call: CallbackQuery, state: FSMContext):
        """
            обробники відповідає на кнопку з назвою Мяза та визначенний callback
            та повертає назву на посилання та відео з виконанням вправи + пагінация
        """
        await state.update_data(muscle_id=func.CALL_MUSCLE_GROUP.get(call.data))
        data = await state.get_data()
        # await state.clear()
        res = await self.db_manager.sports_trein(muscl_id=data.get('muscle_id'))
        await call.message.edit_text(f'<b>Назва<a href="{res[0][1]}">:</a></b> {res[0][0]}',
                                     reply_markup=fabrics.paginator_muscle_worcout())

    async def call_training_with_fitness_bands(self, call: CallbackQuery):
        pass

    def run(self):
        self.dp.callback_query.register(self.cmd_workouts, F.data == "workouts")
        self.dp.callback_query.register(self.cmd_list_workout, F.data == "fitness_menu")
        self.dp.callback_query.register(self.cmd_muscle_name, F.data.in_(
            ["muscle2", "muscle1", "muscle3", "muscle4", "muscle5",
             "muscle6", "muscle7", "muscle8", "muscle9", "muscle10"]),
                                        MuscleIDs.muscle_id)
