from aiogram import F, Bot, Dispatcher
from aiogram.types import CallbackQuery
from database.database import DatabaseManager
from fitnesbot.keybords import fabrics, inline
from fitnesbot.utils import func
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from fitnesbot.utils.states import ADG
from fitnesbot.utils.basemodel import BasicInitialisation


class TrainingFromAthletes(BasicInitialisation):
    def __init__(self, bot: Bot, dp: Dispatcher, db_manager: DatabaseManager):
        super().__init__(bot, dp, db_manager)

    async def cmd_workout_programmes_from_athletes(self, call: CallbackQuery, state: FSMContext):
        """
        обробники відповідає на кнопку 'Програми тренувань від спортсменів' та callback training_from_athletes
        та повертає Inline клавіатуру з тренуваннями від різних спортсменів
        """
        # user_id = call.from_user.id  # Отримуємо ідентифікатор користувача
        # Перевіряємо, чи користувач вже існує у словнику, і якщо ні, ініціалізуємо дані
        # if user_id not in self.user_data:
        #     self.user_data[user_id] = (func.WorkoutAthletes(), func.WorkoutDay(), func.MuscleGroup())
        # await state.set_state(WorkoutAthletes1.sportsman_name)
        await state.set_state(ADG.sportsman_name)
        await call.message.edit_text(f'Виберіть, чію програму тренувань ви хочете подивитися',
                                     reply_markup=inline.training_programmes_from_athletes)
        await call.answer()

    async def cmd_workout_athlete(self, call: CallbackQuery, state: FSMContext):
        """
        обробники відповідає на кнопку з тренуванямс від спортсмена та визначенний callback "ar1 ..."
        та повертає Inline клавіатуру з днями тренувань
        """
        # user_id = call.from_user.id
        # athlete, workout_day, muscle_group = self.user_data[user_id]  # Отримуємо дані користувача
        # es = await self.db_manager.workout_day(call.data)
        # athlete.sportsman_name = call.data
        await state.update_data(sportsman_name=call.data)
        d = await state.get_data()
        print(f"d: {d}")
        await state.set_state(ADG.workout_day_athletes)
        print(call.data)
        # await state.clear()
        res = await self.db_manager.workout_day(d.get('sportsman_name'))
        print(res)
        await call.message.edit_text(f'Виберай день тренування',
                                     reply_markup=fabrics.inline_builder_sql(res, sizes=1,
                                                                             add_cb='training_from_athletes'))
        await call.answer()

    async def cmd_workout_day_athlete(self, call: CallbackQuery, state: FSMContext):
        """
        обробники відповідає на кнопку з днями тренувань та визначенний callback "mondaytothursday ..."
        та повертає Inline клавіатуру з мязами які тренують в цей день
        """
        # user_id = call.from_user.id
        # athlete, workout_day, muscle_group = self.user_data[user_id]
        # print(call.data)
        # workout_day.workout_day = call.data  # Змінюємо атрибут конкретного користувача
        # res = await self.db_manager.muscle_class(athlete.sportsman_name, call.data)
        await state.update_data(workout_day_athletes=call.data)
        d = await state.get_data()
        print(f"d: {d}")
        await state.set_state(ADG.muscle_group_athletes)
        res = await self.db_manager.muscle_class(d.get('sportsman_name'), d.get('workout_day_athletes'))
        await call.message.edit_text(f"Вибери групу м'язів",
                                     reply_markup=fabrics.build_inline_keyboard(res, add_cb='training_from_athletes'))
        await call.answer()

    async def cmd_muscle_group(self, call: CallbackQuery, state: FSMContext):
        """
        обробники відповідає на кнопку з назвою мяза та визначенний callback "hrydy ..."
        та повертає фото вправи іншу інформацію + пагінация та кнопка з посаланням на відео з вправою
        """
        # user_id = call.from_user.id
        # athlete, workout_day, muscle_group = self.user_data[user_id]
        # d = {'hrydy': 'Гриди', 'bitseps': 'Біцепс', 'spyna': 'Спина', 'pres': 'Прес', 'plechy': 'Плечи',
        #      'trytseps': 'Трицепс', 'peredplichchya': 'Передпліччя', 'nohy': 'Ноги', 'ikry': 'Ікри'}
        print(call.data)
        # Змінюємо атрибут конкретного користувача
        # muscle_group.muscle_group = func.CALL_MUSCLE_GROUP_IN_TRAINER[call.data]
        # result_from_sql = await self.db_manager.workout_exercises(athlete.sportsman_name, workout_day.workout_day,
        #                                                    muscle_group.muscle_group)
        await state.update_data(muscle_group_athletes=func.CALL_MUSCLE_GROUP_IN_TRAINER[call.data])
        d = await state.get_data()
        print(f"d: {d}")
        result_from_sql = await self.db_manager.workout_exercises(d.get('sportsman_name'), d.get('workout_day_athletes'),
                                                                  d.get('muscle_group_athletes'))
        print(result_from_sql)
        await call.message.edit_text(f'Назва вправи<a href="{result_from_sql[0][0]}">:</a> {result_from_sql[0][1]}\n'
                                     f'Підходи: {result_from_sql[0][2]}\n'
                                     f'Повторення: {result_from_sql[0][3]}',
                                     reply_markup=fabrics.paginator_muscle(result_from_sql[0][-1]))
        await call.answer()

    async def paginator_muscle_workout(self,
                                       call: CallbackQuery,
                                       callback_data: fabrics.Paginationmuscle,
                                       state: FSMContext):
        """
        Пагінация до cmd_muscle_group
        """
        # user_id = call.from_user.id
        # athlete, workout_day, muscle_group = self.user_data[user_id]
        # exercise = await self.db_manager.workout_exercises(athlete.sportsman_name, workout_day.workout_day,
        #                                                    muscle_group.muscle_group)
        d = await state.get_data()
        print(f"d: {d}")
        exercise = await self.db_manager.workout_exercises(d.get('sportsman_name'), d.get('workout_day_athletes'),
                                                           d.get('muscle_group_athletes'))
        print(exercise)
        page_num = int(callback_data.page)
        page = page_num - 1 if page_num > 0 else 0

        if callback_data.action == 'next_ma':
            page = page_num + 1 if page_num < (len(exercise) - 1) else page_num

        with suppress(TelegramBadRequest):
            await call.message.edit_text(
                f'Назва вправи<a href="{exercise[page][0]}">:</a> {exercise[page][1]}\nПідходи: {exercise[page][2]}\n'
                f'Повторення: {exercise[page][3]}',
                reply_markup=fabrics.paginator_muscle(exercise[page][-1], page))
        await call.answer()

    def run(self):
        self.dp.callback_query.register(self.cmd_workout_programmes_from_athletes, F.data == "training_from_athletes")
        self.dp.callback_query.register(self.cmd_workout_athlete, F.data.in_(["ar1", "ar2"]), ADG.sportsman_name)
        self.dp.callback_query.register(self.cmd_workout_day_athlete,
                                        F.data.in_(["mondaytothursday", "tuesdayandriday", "wednesdayandsaturday",
                                                    "mondayandfriday", "tuesday", "wednesday", "thursday", "saturday"]),
                                        ADG.workout_day_athletes)
        self.dp.callback_query.register(self.cmd_muscle_group, F.data.in_(
            ["hrydy", "bitseps", "spyna", "pres", "plechy", "trytseps", "peredplichchya", "nohy", "ikry"]),
                                        ADG.muscle_group_athletes)
        self.dp.callback_query.register(self.paginator_muscle_workout,
                                        fabrics.Paginationmuscleatlets.filter(F.action.in_(['preliminary_ma',
                                                                                            'next_ma'])))
