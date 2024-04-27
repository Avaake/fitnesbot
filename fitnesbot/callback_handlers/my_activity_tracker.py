from fitnesbot.utils.basemodel import BasicInitialisationBot
from aiogram import F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from fitnesbot.keybords.inline import my_time_workout_inline_menu, my_activity_tracker_menu
from fitnesbot.utils.func import TimeModel
from fitnesbot.utils.states import MyWorkoutTimeState
from fitnesbot.keybords.fabrics import inline_back_button


class MyActivityTracker(BasicInitialisationBot):

    async def my_activity_tracker_handler(self, call: CallbackQuery) -> None:
        await call.message.edit_text(text="Це твій трекер активності. Тицяй на одну з кнопок та продовжуй",
                                     reply_markup=my_activity_tracker_menu)
        await call.answer()

    async def my_time_workout_commands_handler(self, call: CallbackQuery) -> None:
        """Меню для маніпуляції з часом тренувань"""
        await call.message.edit_text(
            text="Привіт! Тут ти зможешь додавати час проведених "
                 "тренувань щоб потім отримувати  аналітику за неділю або місяць",
            reply_markup=my_time_workout_inline_menu)
        await call.answer()

    async def add_the_time_spent_workout_start_handler(self, call: CallbackQuery, state: FSMContext) -> None:
        """Запускаэ MyWorkoutTimeState.my_workout_time та просить користувача вести час тренування"""
        await state.set_state(MyWorkoutTimeState.my_workout_time)
        await call.message.edit_text(text="""
        Введіть час проведенного тренування.
        Формат: <b>Година(01-24),хвилина(01-60)</b>
        """, reply_markup=inline_back_button(title="Назад", callback_title="my_time_workout_commands"))
        await call.answer()

    async def add_the_time_spent_workout_end_handler(self, message: Message, state: FSMContext) -> None:
        """Оновлює MyWorkoutTimeState.my_workout_time робить валідацію та додає дату до БД"""
        await state.update_data(my_workout_time=message.text)
        data = await state.get_data()
        try:
            time_value_one, time_value_two = data['my_workout_time'].split(',')
            if TimeModel(time_value=f"{time_value_one}:{time_value_two}"):
                await self.db_manager.add_time_my_workout(
                    time_workout=str(time_value_one+':'+time_value_two),
                    telegra_id=message.from_user.id)
                await message.answer(f"Час тренування було додано",
                                     reply_markup=inline_back_button(title="⬅ Назад",
                                                                     callback_title="my_time_workout_commands"))
                del data['my_workout_time']
                await state.set_data(data)
        except ValueError:
            await message.answer(
                """
                Не правильний формат часу! Можно використовувати лище цисла 
                Правильний формат: <b>Година(01-24),хвилина(01-60)</b>""",
                reply_markup=inline_back_button(title="⬅ Назад",
                                                callback_title="my_time_workout_commands"))
            del data['my_workout_time']
            await state.set_data(data)

    async def edit_workout_time_message(self, call: CallbackQuery, period: str, response: list[str]):
        minutes = [int(x[:2]) * 60 + int(x[3:]) for x in response]
        average_time = sum(minutes) / len(minutes)

        await call.message.edit_text(text=f"""Дані по часу тренування за {period}
        Середній час: <b>{int(average_time / 60):02}:{int(average_time % 60):02}</b>
        Максімальний час: <b>{max(response)}</b>
        Мінімальний час: <b>{min(response)}</b>
        """, reply_markup=inline_back_button(title="⬅ Назад", callback_title="my_time_workout_commands"))

    async def analytics_of_training_time_for_the_last_7_days(self, call: CallbackQuery) -> None:
        response = await self.db_manager.training_time_in_the_last_7_days(telegram_id=call.from_user.id)
        await self.edit_workout_time_message(call=call, period="остані 7 днів", response=response)

    async def analytics_of_training_time_for_the_last_month(self, call: CallbackQuery) -> None:
        response = await self.db_manager.training_time_in_the_last_month(telegram_id=call.from_user.id)
        await self.edit_workout_time_message(call=call, period="останії місяць", response=response)

    async def run(self):
        self.dp.callback_query.register(self.my_activity_tracker_handler, F.data == "activity_trackers_call")
        self.dp.callback_query.register(self.my_time_workout_commands_handler, F.data == "my_time_workout_commands")
        self.dp.callback_query.register(self.add_the_time_spent_workout_start_handler,
                                        F.data == "add_the_time_spent_training_call")
        self.dp.message.register(self.add_the_time_spent_workout_end_handler, MyWorkoutTimeState.my_workout_time)
        self.dp.callback_query.register(self.analytics_of_training_time_for_the_last_7_days,
                                        F.data == "analytics_of_training_last_7_days")
        self.dp.callback_query.register(self.analytics_of_training_time_for_the_last_month,
                                        F.data == "analytics_of_training_last_month")
