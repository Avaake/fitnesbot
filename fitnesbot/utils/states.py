from aiogram.fsm.state import StatesGroup, State


class ProductFPC(StatesGroup):
    product_name = State()
    calorie_value = State()
    fats = State()
    proteins = State()
    carbohydrates = State()


class ADG(StatesGroup):
    sportsman_name = State()
    workout_day_athletes = State()
    muscle_group_athletes = State()


class MuscleIDs(StatesGroup):
    muscle_id = State()


class TrainingAtHomeCall(StatesGroup):
    title_call = State()


class CreateMyWorkout(StatesGroup):
    my_workout_day = State()
    my_muscle_group = State()
    my_sporting_exercise = State()


class MyWorkoutProgrammeDay(StatesGroup):
    my_training_programme_day = State()


class MyWorkoutTimeState(StatesGroup):
    my_workout_time = State()


class LetterToTechnicalSupport(StatesGroup):
    letter_in_support = State()
