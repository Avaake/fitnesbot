from aiogram.fsm.context import FSMContext

from fitnesbot.utils.basemodel import BasicInitialisationBot
from aiogram import F
from aiogram.types import CallbackQuery
from fitnesbot.keybords.inline import my_account_menu
from fitnesbot.keybords.fabrics import inline_builder_sql, pagination_my_sports_exercises_in_training_kb, \
    playlists_menu, pagination_my_training_programme_sport_exercise_kb
from fitnesbot.keybords import builders
from fitnesbot.utils.states import CreateMyWorkout, MyWorkoutProgrammeDay
from fitnesbot.utils.func import MY_WORKOUT_DAY, CALL_MUSCLE_GROUP


class MyAccount(BasicInitialisationBot):
    async def my_account_cmd(self, call: CallbackQuery):
        """
            Повертає Inline клавіатуру особистого кабінету
        """
        await call.message.edit_text(text=f"Привіт {call.from_user.first_name}! Це твій особистий кабінет. "
                                          f"Можеш починати тичяти по кнопкам", reply_markup=my_account_menu)
        await call.answer()

    async def my_training_account(self, call: CallbackQuery) -> None:
        """
            Перевіряє тренування якщо є то певертає тренування, якщо немає
            то пропонує створити тренування
        """
        response = await self.db_manager.check_if_the_user_has_any_training(call.from_user.id)
        if response[0] == 0:
            recommendation_response = await self.db_manager.view_the_index_of_recommendations(call.from_user.id)
            rec_text = "Увімкнути рекомендації 🔔💡" if recommendation_response == 0 else "Вимкнути рекомендації 🔕💡"
            button_list = [("Створити тренування 🏋️‍♂️✏️", "create_training")]
            await call.message.edit_text(
                text="Так як у вас не має тренування ви можете його створити, "
                     "але тренування може бути лише одне на акаунт, "
                     "щоб створити інше потрібно спочатку видалити існуюче",
                reply_markup=inline_builder_sql(button_list, sizes=1, back_cb="my_account",
                                                add_text=rec_text, add_cb="recommendations_for_the_disease"))
        else:
            button_list = [("Моє тренування 💪🏋️‍♂️", "my_training_programme_day"),
                           ("Видалити тренування 🗑️🏋️‍♂️", "delete_my_training_account"), ]
            await call.message.edit_text(text="Тренування",
                                         reply_markup=inline_builder_sql(button_list, sizes=1, back_cb="my_account"))

    async def create_my_workout(self, call: CallbackQuery, state: FSMContext):
        """
            почитає створення тренування для користувача,
            response перевірє чиє у користувача рекомендації щодо захворювань
            esponse == 0 просимо спочатку обрати захворювання
        """
        response = await self.db_manager.check_uses_disease(call.from_user.id)

        if response == 0:
            await call.message.delete()
            await self.bot.send_message(
                call.from_user.id,
                text="Привіт! Спочатку тицяй на кнопку та вибери всі захворювання які в тебе є, "
                     "щоб отримати рекоментації по спортивним впраа",
                reply_markup=builders.web_keyboard_builder(txt="Спочатку вибери свої захворювання",
                                                           webapp="/users/disease")
            )
        else:
            # await call.message.delete()
            response = await self.db_manager.my_workout_day()
            await state.set_state(CreateMyWorkout.my_workout_day)
            await self.bot.send_message(call.from_user.id, text="Обирай день тренування",
                                        reply_markup=inline_builder_sql(response, back_cb="my_account_workout"))

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
                                     reply_markup=inline_builder_sql(response, sizes=3, back_cb="my_account"))

    async def create_my_workout_load_muscle_group(self, call: CallbackQuery, state: FSMContext):
        """
            Повертає відео та назву вправи + пагінация
            обновляєт CreateMyWorkout.muscle_group
            recommendation_response мустить індекс рекомеднації користувача (on/off)
            recommendation_response == 1 тоді отриміемо id противоказанань по спотривних вправах
        """
        muscle_id = CALL_MUSCLE_GROUP.get(call.data)
        recommendation_response = await self.db_manager.view_the_index_of_recommendations(call.from_user.id)
        if recommendation_response == 1:
            response = await self.db_manager.exercises_that_are_not_recommended_for_the_disease(call.from_user.id)
            if response is not None:
                exercise_id_list = [j for i in response for j in i]
            else:
                exercise_id_list = 0
            response_sports_exercises = await self.db_manager.my_sports_exercises_in_training(
                muscle_id=muscle_id, exercise_ids=exercise_id_list)
        else:
            response_sports_exercises = await self.db_manager.my_sports_exercises_in_training(muscle_id=muscle_id,
                                                                                              exercise_ids=0)
        await state.update_data(my_muscle_group=muscle_id)
        await state.set_state(CreateMyWorkout.my_sporting_exercise)
        await state.update_data(my_sporting_exercise=response_sports_exercises[0][1])
        await call.message.edit_text(
            text=f'<b>Назва<a href="{response_sports_exercises[0][0]}">:</a></b> {response_sports_exercises[0][1]}',
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
        """
            повертає меню з музичними плейлистами
        """
        response = await self.db_manager.music_playlists()
        await call.message.edit_text("Ось плейлисти Spotify для вашого тренування. Приємного прослуховування",
                                     reply_markup=playlists_menu(response))
        await call.answer()

    async def updating_the_user_recommendation_index(self, call: CallbackQuery) -> None:
        """
            вмикаємо або вимекаємо рекомендації для заданого користувача
        """
        recommendation_response = await self.db_manager.view_the_index_of_recommendations(call.from_user.id)
        await self.db_manager.update_the_recommendation_index(rec_index=1 if recommendation_response == 0 else 0,
                                                              telegram_id=call.from_user.id)
        await call.answer(
            "Рекомендації було увімкнуто" if recommendation_response == 0 else "Рекомендації було вимкнуто")
        await self.my_training_account(call=call)

    async def delete_my_workout(self, call: CallbackQuery):
        """
            Видаляє іннуючі тренування
        """
        await self.db_manager.delete_user_workout(call.from_user.id)
        await call.answer(text="Ваше тренування було видалено!!!")

    async def the_day_of_my_training_programme(self, call: CallbackQuery, state: FSMContext):
        await state.set_state(MyWorkoutProgrammeDay.my_training_programme_day)
        response = await self.db_manager.my_training_program_training_day(telegram_id=call.from_user.id)
        await call.message.edit_text(text="Це дні тренування вашої програми",
                                     reply_markup=inline_builder_sql(buttons=response, back_cb="my_account_workout"))

    async def a_sporting_exercise_in_my_training_programme(self, call: CallbackQuery, state: FSMContext):
        await state.update_data(my_training_programme_day=call.data)
        response = await self.db_manager.my_training_programme_sport_exercise(telegram_id=call.from_user.id,
                                                                              call_workout_day=call.data)
        await call.message.edit_text(text=f'<b>Назва<a href="{response[0][0]}">:</a></b> {response[0][1]}',
                                     reply_markup=pagination_my_training_programme_sport_exercise_kb())
        await call.answer()

    async def run(self):
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
        self.dp.callback_query.register(self.updating_the_user_recommendation_index,
                                        F.data == "recommendations_for_the_disease")
        self.dp.callback_query.register(self.the_day_of_my_training_programme, F.data == "my_training_programme_day")
        self.dp.callback_query.register(self.a_sporting_exercise_in_my_training_programme, F.data.in_([
            'call_worckout_day_monday', 'call_worckout_day_tuesday', 'call_worckout_day_wednesday',
            'call_worckout_day_thursday', 'call_worckout_day_friday', 'call_worckout_day_saturday',
            'call_worckout_day_sunday']), MyWorkoutProgrammeDay.my_training_programme_day)
        self.dp.callback_query.register(self.delete_my_workout, F.data == "delete_my_training_account")
        self.dp.callback_query.register(self.playlists_menu, F.data == "Playlists")
