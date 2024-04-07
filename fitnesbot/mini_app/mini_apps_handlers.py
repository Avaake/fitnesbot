from aiogram import Bot, Dispatcher, F
from aiogram.types import WebAppData, CallbackQuery
from database.database import DatabaseManager
from fitnesbot.keybords import builders
from fitnesbot.utils.basemodel import BasicInitialisation
import json
from typing import List


class TelegramMiniAppsHandlers(BasicInitialisation):
    def __init__(self, bot: Bot, dp: Dispatcher, db_manager: DatabaseManager):
        super().__init__(bot, dp, db_manager)

    async def nutrient_calculator_handler(self, call: CallbackQuery) -> None:
        await call.message.answer(
            text="Це калькулятор поживних речовин (КБЖВ) який "
                 "порахує потрібну тобі норму калорій для твого способу життя. <b>Тицяй на кнопку</b>",
            reply_markup=builders.web_keyboard_builder(txt="🧮 Калькулятор калорій та БЖВ", webapp="/users/calcbzy"))
        await call.answer()

    @classmethod
    def __nutrient_calculator(cls,
                              age: int,
                              weight: int,
                              growth: int,
                              gender: str,
                              activity_level: str,
                              goal: str) -> List[int]:
        activity_level_dict = {"sedentary": 1.2, "moderate": 1.375, "active": 1.55, "high": 1.725, "extra": 1.9}
        goal_dict = {"maintenance": 1.0, "weight_loss": 0.85, "weight_gain": 1.15}
        BMR = 0
        # BMR = 88, 362 + (13, 397 × вес в кг) + (4, 799 × рост в см) - (5, 677 × возраст в годах) male
        # BMR = 447,593 + (9,247 × вес в кг) + (3,098 × рост в см) - (4,330 × возраст в годах) female
        match gender:
            case "male":
                BMR = 88.362 + (13.397 * weight) + (4.799 * growth) - (5.677 * age)
            case "female":
                BMR = 447.593 + (9.247 * weight) + (3.098 * growth) - (4.330 * age)

        AMR = activity_level_dict.get(activity_level, 1.2)
        goal_multiplier = goal_dict.get(goal, 1.0)

        calories = round(AMR * BMR * goal_multiplier)
        proteins = round((0.15 * calories) / 4)
        fets = round((0.25 * calories) / 9)
        carbohydrates = round((0.60 * calories) / 4)

        result = [calories, proteins, fets, carbohydrates]
        return result

    async def nutrient_calculator_web_handler(self, web_mess_data: WebAppData) -> None:
        data = json.loads(web_mess_data.web_app_data.data)
        res = self.__nutrient_calculator(
            age=int(data.get("age")),
            weight=int(data.get("weight")),
            growth=int(data.get("growth")),
            gender=data.get("gender"),
            activity_level=data.get("activity_level"),
            goal=data.get("goal")
        )
        await self.bot.send_message(web_mess_data.chat.id,
                                    f"Добова норма калорій за формулою Харріса-Бенедикта становить: "
                                    f"<b>{res[0]}</b> калорій"
                                    f"\n\t<b>Білки: {res[1]}</b> грамів."
                                    f"\n\t<b>Жири: {res[2]}</b> грамів."
                                    f"\n\t<b>Вуглеводи: {res[-1]}</b> грамів.",
                                    reply_markup=builders.cancel_kb)

    async def selection_of_diseases(self, call: CallbackQuery) -> None:
        await call.message.answer(text="Нажимай на кнопку та вибери всі захваорювання які в тебе є",
                                  reply_markup=builders.web_keyboard_builder(txt="Вибір присутніх захворювань",
                                                                             webapp="/users/disease"))

    async def selection_of_diseases_web_handler(self, web_mess_data: WebAppData) -> None:
        data = json.loads(web_mess_data.web_app_data.data)
        print(data)
        await self.bot.send_message(web_mess_data.chat.id,
                                    f'Захворювання: {data.get("hernia")}',
                                    reply_markup=builders.cancel_kb)

    def run(self) -> None:
        self.dp.callback_query.register(self.nutrient_calculator_handler, F.data == "nutrientcalculator")
        self.dp.callback_query.register(self.selection_of_diseases, F.data == "selectiondiseases")
        self.dp.message.register(self.nutrient_calculator_web_handler,
                                 F.web_app_data.button_text == "🧮 Калькулятор калорій та БЖВ")
        self.dp.message.register(self.selection_of_diseases_web_handler,
                                 F.web_app_data.button_text == "Вибір присутніх захворювань")
