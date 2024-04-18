from fitnesbot.utils.basemodel import BasicInitialisationBot
from aiogram import F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandObject, Command
from aiogram.fsm.context import FSMContext
from fitnesbot.keybords.inline import my_time_workout_inline_menu
from fitnesbot.utils.func import TimeModel
from fitnesbot.utils.states import MyWorkoutTimeState
from fitnesbot.keybords.fabrics import inline_back_button


class MyWorkoutTime(BasicInitialisationBot):
    async def my_time_workout_commands_handler(self, call: CallbackQuery) -> None:
        await call.message.edit_text(
            text="Привіт! Тут ти зможешь додавати час проведених "
                 "тренувань щоб потім отримувати  аналітику за неділю або місяць",
            reply_markup=my_time_workout_inline_menu)
        await call.answer()

    async def add_the_time_spent_workout_start_handler(self, call: CallbackQuery, state: FSMContext) -> None:
        await state.set_state(MyWorkoutTimeState.my_workout_time)
        await call.message.edit_text(text="""
        Введіть час проведенного тренування.
        Формат: <b>Година(01-24),хвилина(01-60)</b>
        """, reply_markup=inline_back_button(title="Назад", callback_title="my_time_workout_commands"))
        await call.answer()

    async def add_the_time_spent_workout_end_handler(self, message: Message, state: FSMContext) -> None:
        await state.update_data(my_workout_time=message.text)
        data = await state.get_data()
        try:
            time_value_one, time_value_two = data['my_workout_time'].split(',')
            if TimeModel(time_value=f"{time_value_one}:{time_value_two}"):
                await message.answer(f"було додано",
                                     reply_markup=inline_back_button(title="Назад",
                                                                     callback_title="my_time_workout_commands"))
                del data['my_workout_time']
                await state.set_data(data)
        except ValueError as e:
            await message.answer(
                """
                Не правильний формат часу! Можно використовувати лище цисла 
                Правильний формат: <b>Година(01-24),хвилина(01-60)</b>""",
                reply_markup=inline_back_button(title="Назад",
                                                callback_title="my_time_workout_commands"))
            del data['my_workout_time']
            await state.set_data(data)

    async def run(self):
        self.dp.callback_query.register(self.my_time_workout_commands_handler, F.data == "my_time_workout_commands")
        self.dp.callback_query.register(self.add_the_time_spent_workout_start_handler,
                                        F.data == "add_the_time_spent_training_call")
        self.dp.message.register(self.add_the_time_spent_workout_end_handler, MyWorkoutTimeState.my_workout_time)
