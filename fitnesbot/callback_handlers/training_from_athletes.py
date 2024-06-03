from aiogram import F
from aiogram.types import CallbackQuery
from fitnesbot.keybords import fabrics, inline
from fitnesbot.utils import func
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from fitnesbot.utils.states import ADG
from fitnesbot.utils.basemodel import BasicInitialisationBot


class TrainingFromAthletes(BasicInitialisationBot):
    async def cmd_workout_programmes_from_athletes(self, call: CallbackQuery, state: FSMContext):
        """
        обробники відповідає на кнопку 'Програми тренувань від спортсменів' та callback training_from_athletes
        та повертає Inline клавіатуру з тренуваннями від різних спортсменів
        """
        await state.set_state(ADG.sportsman_name)
        await call.message.edit_text(f'Виберіть, чію програму тренувань ви хочете подивитися',
                                     reply_markup=inline.training_programmes_from_athletes)
        await call.answer()

    async def cmd_workout_athlete(self, call: CallbackQuery, state: FSMContext):
        """
        обробники відповідає на кнопку з тренуванямс від спортсмена та визначенний callback "ar1 ..."
        та повертає Inline клавіатуру з днями тренувань
        """
        await state.update_data(sportsman_name=call.data)
        data = await state.get_data()
        await state.set_state(ADG.workout_day_athletes)
        response = await self.db_manager.workout_day(data.get('sportsman_name'))
        await call.message.edit_text(f'Виберай день тренування',
                                     reply_markup=fabrics.inline_builder_sql(response, sizes=1,
                                                                             back_cb='training_from_athletes'))
        await call.answer()

    async def cmd_workout_day_athlete(self, call: CallbackQuery, state: FSMContext):
        """
        обробники відповідає на кнопку з днями тренувань та визначенний callback "mondaytothursday ..."
        та повертає Inline клавіатуру з мязами які тренують в цей день
        """
        await state.update_data(workout_day_athletes=call.data)
        data = await state.get_data()
        await state.set_state(ADG.muscle_group_athletes)
        response = await self.db_manager.muscle_class(data.get('sportsman_name'), data.get('workout_day_athletes'))
        await call.message.edit_text(f"Вибери групу м'язів",
                                     reply_markup=fabrics.build_inline_keyboard(
                                         response,
                                         add_cb='training_from_athletes')
                                     )
        await call.answer()

    async def cmd_muscle_group(self, call: CallbackQuery, state: FSMContext):
        """
        обробники відповідає на кнопку з назвою мяза та визначенний callback "hrydy ..."
        та повертає фото вправи іншу інформацію + пагінация та кнопка з посаланням на відео з вправою
        """
        await state.update_data(muscle_group_athletes=func.CALL_MUSCLE_GROUP_IN_TRAINER[call.data])
        data = await state.get_data()
        response = await self.db_manager.workout_exercises(data.get('sportsman_name'),
                                                           data.get('workout_day_athletes'),
                                                           data.get('muscle_group_athletes'))
        await call.message.edit_text(f'Назва вправи<a href="{response[0][0]}">:</a> {response[0][1]}\n'
                                     f'Підходи: {response[0][2]}\n'
                                     f'Повторення: {response[0][3]}',
                                     reply_markup=fabrics.paginator_muscle(response[0][-1]))
        await call.answer()

    async def paginator_muscle_workout(self,
                                       call: CallbackQuery,
                                       callback_data: fabrics.Paginationmuscle,
                                       state: FSMContext):
        """
            Пагінация до cmd_muscle_group
        """

        data = await state.get_data()
        exercise = await self.db_manager.workout_exercises(data.get('sportsman_name'), data.get('workout_day_athletes'),
                                                           data.get('muscle_group_athletes'))
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

    async def run(self):
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
