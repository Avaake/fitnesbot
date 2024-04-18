from fitnesbot.utils.basemodel import BasicInitialisationBot
from aiogram import F
from aiogram.types import CallbackQuery
from fitnesbot.keybords import inline
from aiogram.fsm.context import FSMContext
from fitnesbot.utils.states import TrainingAtHomeCall
from fitnesbot.keybords import fabrics


class TrainingAtHome(BasicInitialisationBot):
    """
        клас TrainingAtHome працює с тренуваннями для дому
    """

    async def cmd_training_at_home(self, call: CallbackQuery) -> None:
        """
            Обродник для кнопки "Тренування в дома" callback_data=training_at_home,
            повертає інлайн клавіатуру с тренуванняи
        """
        await call.message.edit_text(text="Виберай тренування для дому ", reply_markup=inline.training_at_home_menu)

    async def cmd_training_at_home_day(self, call: CallbackQuery, state: FSMContext):
        await state.set_state(TrainingAtHomeCall.title_call)
        response = await self.db_manager.training_at_home_day(str(call.data))
        print(response)
        await call.message.answer(text=f"Привіт {call.from_user.first_name} обирай тренування для дому",
                                  reply_markup=fabrics.inline_builder_sql(response, back_cb="training_at_home"))

    async def cmd_training_at_home_title(self, call: CallbackQuery, state: FSMContext) -> None:
        """
            Обробник для тренувань повертає інформації про тренування + пагінация
        """
        print(str(call.data))
        response = await self.db_manager.training_at_home(str(call.data))
        await state.update_data(title_call=str(call.data))
        await call.message.edit_text(
            text=f'{response[0][0]}\n<b>Назва вправи<a href="{response[0][1]}">:</a></b> {response[0][2]}'
                 f'\n<b>Кількість підходів:</b> {response[0][3]}\n<b>Кількість повторень:</b> {response[0][4]}\n'
                 f'<b>Відпочинок:</b> {response[0][5]}',
            reply_markup=fabrics.paginator_training_at_home(backwards=response[0][6]))

    async def run(self):
        self.dp.callback_query.register(self.cmd_training_at_home, F.data == "training_at_home", )
        self.dp.callback_query.register(self.cmd_training_at_home_day, F.data.in_([
            "first_training_at_home",
            "second_training_at_home",
            "third_training_at_home"
        ]))
        self.dp.callback_query.register(self.cmd_training_at_home_title, F.data.in_([
            "ftah_three_day_split",
        ]), TrainingAtHomeCall.title_call)
