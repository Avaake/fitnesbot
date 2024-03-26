from aiogram import F, Dispatcher, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from database.database import DatabaseManager
from bot.keybords import fabrics
from contextlib import suppress
from aiogram.types import CallbackQuery
from bot.utils import func
from bot.utils.states import MuscleIDs, TrainingAtHomeCall, CreateMyWorkout
from bot.utils.basemodel import BasicInitialisation

muscle = func.MuscleID


class Pagin(BasicInitialisation):
    """Клас Pagin містить пагінації для інших команд """
    def __init__(self, bot: Bot, dp: Dispatcher, db_manager: DatabaseManager):
        super().__init__(bot, dp, db_manager)

    async def paginator_my_workout(self, call: CallbackQuery, callback_data: fabrics.Pagination):
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
        await state.set_state(CreateMyWorkout.sporting_exercise)
        data = await state.get_data()
        print(data)
        response = await self.db_manager.my_sports_exercises_in_training(data.get('muscle_group'))
        page_num = int(callback_data.page)

        page = page_num - 1 if page_num > 0 else 0

        if callback_data.action == "next_mseit":
            page = page_num + 1 if page_num < (len(response) - 1) else page_num

        await state.update_data(sporting_exercise=response[page][1])
        with suppress(TelegramBadRequest):
            await call.message.edit_text(text=f'<b>Назва<a href="{response[page][0]}">:</a></b> {response[page][1]}',
                                         reply_markup=fabrics.pagination_my_sports_exercises_in_training_kb(page=page))

    def run(self):
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
