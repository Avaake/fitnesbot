from aiogram.fsm.state import StatesGroup, State


class ProductFPC(StatesGroup):
    product_name = State()
    calorie_value = State()
    fats = State()
    proteins = State()
    carbohydrates = State()


class FoodCounting(StatesGroup):
    meal = State()
    food = State()


class ADG(StatesGroup):
    sportsman_name = State()
    workout_day = State()
    muscle_group = State()


class MuscleIDs(StatesGroup):
    muscle_id = State()


class AdditiveNamesCall(StatesGroup):
    additive_name_call = State()


class TrainingAtHomeCall(StatesGroup):
    title_call = State()


class CreateMyWorkout(StatesGroup):
    workout_day = State()
    muscle_group = State()
    sporting_exercise = State()
