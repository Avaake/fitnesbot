from aiogram.fsm.context import FSMContext

from bot.utils.basemodel import BasicInitialisation
from aiogram import Bot, Dispatcher, F
from database.database import DatabaseManager
from aiogram.types import CallbackQuery
from bot.keybords.inline import my_account_menu, playlists_menu
from bot.keybords.fabrics import inline_builder_sql, pagination_my_sports_exercises_in_training_kb
from bot.utils.states import CreateMyWorkout
from bot.utils.func import MY_WORKOUT_DAY, CALL_MUSCLE_GROUP


class MyAccount(BasicInitialisation):
    def __init__(self, bot: Bot, dp: Dispatcher, db_manager: DatabaseManager):
        super().__init__(bot, dp, db_manager)

    async def my_account_cmd(self, call: CallbackQuery):
        """
            Повертає Inline клавіатуру особистого кабінету
        """
        await call.message.edit_text("Це твій особистий кабінет", reply_markup=my_account_menu)
        await call.answer()

    async def my_training_account(self, call: CallbackQuery):
        """
            Перевіряє тренування якщо є то певертає тренування, якщо немає
            то пропонує створити тренування
        """
        response = await self.db_manager.check_if_the_user_has_any_training(call.from_user.id)
        if response[0] == 0:
            button_list = [("Створити тренування", "create_training")]
            await call.message.edit_text(
                text="Так як у вас не має тренування ви можете його створити, "
                     "але тренування може біти лише одне на акаунт, "
                     "щоб створити інше потрібно спочатку видалити існуюче",
                reply_markup=inline_builder_sql(button_list, sizes=1, add_cb="my_account"))
        else:
            button_list = [("Моє тренування", "my_training_account"),
                           ("Видалити тренування", "delete_my_training_account"),]
            await call.message.edit_text(text="Тренування",
                                         reply_markup=inline_builder_sql(button_list, sizes=1, add_cb="my_account"))

    async def create_my_workout(self, call: CallbackQuery, state: FSMContext):
        """
            Створення тренування, Повертає Inline клавіатуру з днями тижня
            та запускає state CreateMyWorkout
        """
        response = await self.db_manager.my_workout_day()
        await state.set_state(CreateMyWorkout.my_workout_day)
        await call.message.edit_text(text="Обирай день тренування",
                                     reply_markup=inline_builder_sql(response, add_cb="my_account_workout"))

    async def create_my_workout_load_workout_day(self, call: CallbackQuery, state: FSMContext):
        """
            Повертає Inline клавіатуру з групами мязів
            обновляєт CreateMyWorkout.workout_day
        """
        response = await self.db_manager.muscle_group_inline()
        await state.update_data(my_workout_day=MY_WORKOUT_DAY.get(call.data))
        await state.set_state(CreateMyWorkout.my_muscle_group)
        data = await state.get_data()
        print(f"create_my_workout_load_workout_day {data}")
        await call.message.edit_text(text="Обирай м'язову групу",
                                     reply_markup=inline_builder_sql(response, sizes=3, add_cb="my_account"))


    async def create_my_workout_load_muscle_group(self, call: CallbackQuery, state: FSMContext):
        """
            Повертає відео та назву вправи + пагінация
            обновляєт CreateMyWorkout.muscle_group
        """
        muscle_id = CALL_MUSCLE_GROUP.get(call.data)
        print(muscle_id)
        response = await self.db_manager.my_sports_exercises_in_training(muscle_id)
        print(response)
        await state.update_data(my_muscle_group=muscle_id)
        await state.set_state(CreateMyWorkout.my_sporting_exercise)
        await state.update_data(my_sporting_exercise=response[0][1])
        await call.message.edit_text(text=f'<b>Назва<a href="{response[0][0]}">:</a></b> {response[0][1]}',
                                     reply_markup=pagination_my_sports_exercises_in_training_kb())

    async def create_my_workout_load_sporting_exercise(self, call: CallbackQuery, state: FSMContext):
        """
            Цей callback додає вправу в тренування(БД)
        """
        data = await state.get_data()
        print(f"create_my_workout_load_sporting_exercise {data}")
        user_id = await self.db_manager.check_telegram_id(call.from_user.id)
        sporting_exercise_id = await self.db_manager.check_sporting_exercise_id(data.get('my_sporting_exercise'))
        await self.db_manager.add_an_exercise_to_my_workout_routine(user_id=user_id,
                                                                    workout_day=data.get('my_workout_day'),
                                                                    muscle_group=data.get('my_muscle_group'),
                                                                    sporting_exercise_id=sporting_exercise_id
                                                                    )
        await call.answer(text=f'Вправа {data.get("my_sporting_exercise")} додана')

    async def playlists_menu(self, call: CallbackQuery):
        await call.message.edit_text("Ось плейлисти Spotify для вашого тренування. Приємного прослуховування",
                                     reply_markup=playlists_menu)
        await call.answer()

    async def delete_my_workout(self, call: CallbackQuery):
        """
            Видаляє іннуючі тренування
        """
        await self.db_manager.delete_user_workout(call.from_user.id)
        await call.answer(text="Ваше тренування було видалено!!!")

    def run(self):
        self.dp.callback_query.register(self.my_account_cmd, F.data == "my_account")
        self.dp.callback_query.register(self.my_training_account, F.data == "my_account_workout")
        self.dp.callback_query.register(self.create_my_workout, F.data == 'create_training')
        self.dp.callback_query.register(self.create_my_workout_load_workout_day, F.data.in_([
            'call_worckout_day_monday', 'call_worckout_day_tuesday', 'call_worckout_day_wednesday',
            'call_worckout_day_thursday', 'call_worckout_day_friday', 'call_worckout_day_saturday',
            'call_worckout_day_sunday']), CreateMyWorkout.my_workout_day)
        self.dp.callback_query.register(self.create_my_workout_load_muscle_group, F.data.in_([
            "muscle2", "muscle1", "muscle3", "muscle4", "muscle5",
            "muscle6", "muscle7", "muscle8", "muscle9", "muscle10"]), CreateMyWorkout.my_muscle_group)
        self.dp.callback_query.register(self.create_my_workout_load_sporting_exercise,
                                        F.data == "add_to_your_workout")
        self.dp.callback_query.register(self.delete_my_workout, F.data == "delete_my_training_account")
        self.dp.callback_query.register(self.playlists_menu, F.data == "Playlists")
