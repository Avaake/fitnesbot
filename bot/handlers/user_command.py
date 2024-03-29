from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandObject
from aiogram.types import ReplyKeyboardRemove, Message, CallbackQuery
from database.database import DatabaseManager
from bot.keybords import fabrics, builders
from bot.keybords.inline import menu
from bot.utils.func import isfloat
from bot.utils.basemodel import BasicInitialisation


class User(BasicInitialisation):
    """
        Клас User містить обробники команд які доступні всім користувачас
    """

    def __init__(self, bot: Bot, dp: Dispatcher, db_manager: DatabaseManager):
        super().__init__(bot, dp, db_manager)

    async def cmd_start(self, message: Message):
        """Обробник команди start"""
        await message.answer(f'Hello {message.from_user.first_name}', reply_markup=menu)
        # await self.bot.send_message(chat_id=message.chat.id, text=f'Hello {message.from_user.first_name}', reply_markup=menu)
        # await self.bot.send_voice(chat_id=message.chat.id, voice="AwACAgIAAxkBAAIao2WudJlIWs5L_rZk9EsbI0nRTjzZAALFQgACwGlwSVO3R24DabGRNAQ")

    async def call_cmd_start(self, call: CallbackQuery):
        """Обробник команди start"""
        await call.message.edit_text(f'Hello {call.message.from_user.first_name}', reply_markup=menu)

    # async def fr1(self, message: Message):
    #     print(message.voice.file_id)
    #     await message.answer_voice(message.voice.file_id)

    async def cmd_video(self, message: Message):
        """Обробник прийає всі відео та повертає його id"""
        print(message.video.file_id)
        await message.answer(message.video.file_id)

    async def cmd_v(self, message: Message):
        """Обробник команди vid відправлаю відео"""
        await message.answer_video('https://cdn.muscleandstrength.com/video/dumbbellpullover.mp4')

    async def cmd_p(self, message: Message):
        """Обробник команди pid відправлаю фото"""
        await message.answer_photo(
            photo='https://encrypted-tbn0.gstatic.com/images?q=tbn'
                  ':ANd9GcS8QfXHtv9Cvd05o5Xicde7PBQNbkgRi8A03OWWew0AXHpJyaUgMAB_Gi9N-sRs5Fa3-II&usqp=CAU')

    async def cnd_my_workout(self, call: CallbackQuery):
        """Обробник команди my_workout поверає список тренувать"""
        exercise = await self.db_manager.sports_exercises()
        print(exercise)
        await call.message.answer(f'page=0\n<b>Вправа: </b>{exercise[0][0]}\n<b>Підходи: </b>{exercise[0][1]}',
                                  reply_markup=fabrics.paginator())
        await call.answer()

    async def cmd_my_workout_class(self, call: CallbackQuery):
        """Обробник команди my_workout_clas поверає список мишц"""
        # r = await self.db_manager.sports_muscles()
        # l = [j
        #      for i in r
        #      for j in i]
        # print(l)
        await call.message.answer("Вибери групу мишц", reply_markup=builders.muscles)

    async def cmd_add_my_workout_time(self, message: Message, command: CommandObject):
        """Обробник команди time_work є треком часу тренування"""
        if command.args is not None:
            workout_time = command.args
            if workout_time.isnumeric() or isfloat(workout_time):
                print(command.args)
                await self.db_manager.add_time_my_workout(workout_time, message.from_user.username)
                await message.answer("Час додано")

    async def cancel_handler(self, message: Message, state: FSMContext):
        """Обробник команди cancel зупиняє state"""
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.clear()
        await message.answer(
            "Cancelled.",
            reply_markup=ReplyKeyboardRemove(),
        )

    def run(self):
        """регеєструє всі обробники """
        self.dp.message.register(self.cmd_start, Command('start'))
        self.dp.callback_query.register(self.call_cmd_start, F.data == 'start')
        # self.dp.message.register(self.fr1, F.voice)
        self.dp.message.register(self.cancel_handler, Command("cancel"))
        self.dp.message.register(self.cmd_video, F.video)
        self.dp.message.register(self.cmd_v, Command('vid'))
        self.dp.message.register(self.cmd_p, Command('pid'))
        self.dp.callback_query.register(self.cnd_my_workout, F.data == "my_workout")
        self.dp.callback_query.register(self.cmd_my_workout_class, F.data == "my_workout_clas")
        self.dp.message.register(self.cmd_add_my_workout_time, Command('time_work'))
