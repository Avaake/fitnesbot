from aiogram import F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from fitnesbot.keybords import fabrics
from contextlib import suppress
from aiogram.types import CallbackQuery
from fitnesbot.utils import func
from fitnesbot.utils.states import MuscleIDs, TrainingAtHomeCall, CreateMyWorkout, MyWorkoutProgrammeDay
from fitnesbot.utils.basemodel import BasicInitialisationBot

muscle = func.MuscleID


class Pagin(BasicInitialisationBot):
    """Клас Pagin містить пагінації для інших команд """

    async def paginator_my_workout(self, call: CallbackQuery, callback_data: fabrics.Pagination):
        """
            В розробці
        """
        response = await self.db_manager.sports_exercises()

        page_num = int(callback_data.page)
        page = page_num - 1 if page_num > 0 else 0

        if callback_data.action == 'next':
            page = page_num + 1 if page_num < (len(response) - 1) else page_num

        with suppress(TelegramBadRequest):
            await call.message.edit_text(
                f'{page=}\n<b>Вправа: </b>{response[page][0]}\n<b>Підходи: </b>{response[page][1]}',
                reply_markup=fabrics.paginator(page))
        await call.answer()

    async def paginator_food(self, call: CallbackQuery, callback_data: fabrics.PaginationFood):
        massage_list = [i.split(': ') for i in call.message.text.split("\n")]
        food_index = await self.db_manager.food_index(massage_list[1][1])
        info_food = await self.db_manager.food_information(*food_index)
        page_num = int(callback_data.page)
        page = page_num - 1 if page_num > 0 else 0

        if callback_data.action == 'next_f':
            page = page_num + 1 if page_num < (len(info_food) - 1) else page_num

        with suppress(TelegramBadRequest):
            await call.message.edit_text(
                f'{page=}\n<b>Назва: </b>{info_food[page][0]}\n<b>Калорисность: </b>{info_food[page][1]}\n'
                f'<b>Билки: </b>{info_food[page][2]}\n<b>Жири: </b>{info_food[page][3]}\n'
                f'<b>Угливоди: </b>{info_food[page][4]}',
                reply_markup=fabrics.paginator_food(page))
        await call.answer()

    async def paginator_muscle_workout(self,
                                       call: CallbackQuery,
                                       callback_data: fabrics.Paginationmuscle,
                                       state: FSMContext):
        """
            Пагінація для перегляду спортивних вправ cmd_muscle_name
        """
        await state.set_state(MuscleIDs.muscle_id)
        data = await state.get_data()
        response = await self.db_manager.sports_trein(muscl_id=data.get('muscle_id'))
        page_num = int(callback_data.page)

        page = page_num - 1 if page_num > 0 else 0

        if callback_data.action == 'next_m':
            page = page_num + 1 if page_num < (len(response) - 1) else page_num
        print(f"page: {page}")
        with suppress(TelegramBadRequest):
            url = response[page][1]
            await call.message.edit_text(
                f'<b>Назва<a href="{url}">:</a></b>{response[page][0]}',
                reply_markup=fabrics.paginator_muscle_worcout(page=page))
        await call.answer()

    async def paginator_training_home(self,
                                      call: CallbackQuery,
                                      callback_data: fabrics.PaginationTrainingAtHome,
                                      state: FSMContext):
        """
            Пагінация для програм тренувань вдома cmd_training_at_home_title
        """
        await state.set_state(TrainingAtHomeCall.title_call)
        data = await state.get_data()
        response = await self.db_manager.training_at_home(training_call=data.get('title_call'))
        page_num = int(callback_data.page)

        page = page_num - 1 if page_num > 0 else 0

        if callback_data.action == "next_triathome":
            page = page_num + 1 if page_num < (len(response) - 1) else page_num

        with suppress(TelegramBadRequest):
            url = response[page][1]
            backwards = response[page][-1]
            await call.message.edit_text(
                text=f'<b>Назва вправи<a href="{url}">:</a></b> {response[page][2]}'
                     f'\n<b>Кількість підходів:</b> {response[page][3]}\n<b>Кількість повторень:</b> '
                     f'{response[page][4]}\n<b>Відпочинок:</b> {response[page][5]}',
                reply_markup=fabrics.paginator_training_at_home(backwards=backwards, page=page)
            )

    async def pagination_my_sports_exercises_in_training(self,
                                                         call: CallbackQuery,
                                                         callback_data: fabrics.PaginationMySportsExercisesInTraining,
                                                         state: FSMContext):
        """
            Пагінація для створення славного плану твенувать create_my_workout_load_muscle_group
        """
        await state.set_state(CreateMyWorkout.my_sporting_exercise)
        data = await state.get_data()
        recommendation_response = await self.db_manager.view_the_index_of_recommendations(call.from_user.id)
        if recommendation_response == 1:
            response = await self.db_manager.exercises_that_are_not_recommended_for_the_disease(call.from_user.id)
            if response is not None:
                exercise_id_list = [j for i in response for j in i]
            else:
                exercise_id_list = 0
            response_sports_exercises = await self.db_manager.my_sports_exercises_in_training(
                muscle_id=data.get('my_muscle_group'),
                exercise_ids=exercise_id_list)
        else:
            response_sports_exercises = await self.db_manager.my_sports_exercises_in_training(
                muscle_id=data.get('my_muscle_group'),
                exercise_ids=0)

        page_num = int(callback_data.page)
        page = page_num - 1 if page_num > 0 else 0

        if callback_data.action == "next_mseit":
            page = page_num + 1 if page_num < (len(response_sports_exercises) - 1) else page_num

        await state.update_data(my_sporting_exercise=response_sports_exercises[page][1])
        with suppress(TelegramBadRequest):
            await call.message.edit_text(
                text=f'<b>Назва<a href="{response_sports_exercises[page][0]}">:</a></b> '
                     f'{response_sports_exercises[page][1]}',
                reply_markup=fabrics.pagination_my_sports_exercises_in_training_kb(page=page))

    async def paginator_a_sporting_exercise_in_my_training_programme(self,
                                                                     call: CallbackQuery,
                                                                     callback_data:
                                                                     fabrics.PaginationMyTrainingProgrammeSportExercise,
                                                                     state: FSMContext) -> None:
        """
            Пагінация для перегляду власного тренування a_sporting_exercise_in_my_training_programme
        """
        await state.set_state(MyWorkoutProgrammeDay.my_training_programme_day)
        data = await state.get_data()
        response = await self.db_manager.my_training_programme_sport_exercise(
            telegram_id=call.from_user.id,
            call_workout_day=data.get("my_training_programme_day"))
        page_num = int(callback_data.page)

        page = page_num - 1 if page_num > 0 else 0

        if callback_data.action == "next_mtpsek":
            page = page_num + 1 if page_num < (len(response) - 1) else page_num

        with suppress(TelegramBadRequest):
            await call.message.edit_text(text=f'<b>Назва<a href="{response[page][0]}">:</a></b> {response[page][1]}',
                                         reply_markup=fabrics.pagination_my_training_programme_sport_exercise_kb(
                                             page=page))

    async def pagination_to_view_recipes(self,
                                         call: CallbackQuery,
                                         callback_data:
                                         fabrics.PaginationToViewRecipes
                                         ) -> None:
        response = await self.db_manager.recipes_information()
        page_num = int(callback_data.page)

        page = page_num - 1 if page_num > 0 else 0

        if callback_data.action == "next_tovr":
            page = page_num + 1 if page_num < (len(response) - 1) else page_num

        with suppress(TelegramBadRequest):
            await call.message.edit_text(text=f'<b>Назва<a href="{response[page][1]}">:</a></b> {response[page][2]}'
                                              f'<b>Інгредієнти</b> {response[page][3]}',
                                         reply_markup=fabrics.pagination_to_view_recipes_kb(page=page))

    async def run(self):
        self.dp.callback_query.register(self.paginator_my_workout,
                                        fabrics.Pagination.filter(F.action.in_(['preliminary', 'next'])))
        self.dp.callback_query.register(self.paginator_food,
                                        fabrics.PaginationFood.filter(F.action.in_(['preliminary_f', 'next_f'])))
        self.dp.callback_query.register(self.paginator_muscle_workout,
                                        fabrics.Paginationmuscle.filter(F.action.in_(['preliminary_m', 'next_m'])))
        self.dp.callback_query.register(self.paginator_training_home,
                                        fabrics.PaginationTrainingAtHome.filter(F.action.in_(['preliminary_triathome',
                                                                                              'next_triathome'])))
        self.dp.callback_query.register(self.pagination_my_sports_exercises_in_training,
                                        fabrics.PaginationMySportsExercisesInTraining.filter(F.action.in_(
                                            ['preliminary_mseit', 'next_mseit'])))
        self.dp.callback_query.register(self.paginator_a_sporting_exercise_in_my_training_programme,
                                        fabrics.PaginationMyTrainingProgrammeSportExercise.filter(F.action.in_(
                                            ['preliminary_mtpsek', 'next_mtpsek'])))
        self.dp.callback_query.register(self.paginator_a_sporting_exercise_in_my_training_programme,
                                        fabrics.PaginationToViewRecipes.filter(F.action.in_(
                                            ['preliminary_tovr', 'next_tovr'])))
