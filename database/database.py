import asyncio
import logging

from typing import List
from math import ceil
import aiomysql
from config import settings


def calorie_calculation(x, y):
    return (float(x) / float(100)) * float(y)


class DatabaseManager:
    """
    Клас DatabaseManager використовується для підключення до бази даних MySQL,
    містить паттерн Singleton, який не допускає більше одного екземпляру класу,
    виконується з допомогою тандемних методів __new__ та __del__. Також є конструкція __init__
    яка містить host, user, password, database та підключення до бази даних mydb
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __del__(self):
        self._instance = None

    def __init__(self):
        self.__host = settings.host
        self.__port = settings.port
        self.__user = settings.user
        self.__password = settings.password
        self.__database = settings.database_name
        self.__mydb = None

    async def connect_db(self):
        """робить конект до Database"""
        if self.__mydb is None:
            try:
                self.__mydb = await aiomysql.connect(
                    host=self.__host,
                    port=self.__port,
                    user=self.__user,
                    password=self.__password,
                    db=self.__database,
                    loop=asyncio.get_event_loop()
                )
                print('Database connected!')
            except aiomysql.Error as exc:
                logging.critical(f"{exc}")

    async def disconnect_db(self):
        """виконує дісконект """
        if self.__mydb:
            self.__mydb.close()
            print('Database disconnected!')

    async def verify_the_user_through_middleware(self, telegram_id: int):
        try:
            sql_command = """
                SELECT count(telegram_id) 
                FROM fitnesdb.users
                WHERE telegram_id = %s
            """
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (telegram_id,))
                data = await cursor.fetchone()
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def add_the_user_through_middleware(self, telegram_id: int, first_name: str,
                                              user_name: str, language_code: str):
        try:
            sql_command = """
                INSERT INTO users (telegram_id, first_name, user_name, language_code)
                VALUES (%s, %s, %s, %s)
            """
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (telegram_id, first_name, user_name, language_code))
                await self.__mydb.commit()  # Очікуйте завершення асинхронного commit
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def update_last_date_the_user_through_middleware(self, telegram_id: int):
        try:
            sql_command = """
                UPDATE users SET last_update = CURRENT_TIMESTAMP
                WHERE telegram_id = %s
            """
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (telegram_id,))
                await self.__mydb.commit()
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def add_products(self, username: str, *args: List):
        try:

            sql_command = """INSERT INTO products (product_name, calorie_value, fats, proteins, carbohydrates, users) 
                             VALUES (%s, %s, %s, %s, %s, %s)"""
            values = list(*args)
            values.append(username)

            print(values)
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, values)
            await self.__mydb.commit()
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def func(self, pram):
        try:
            sql_command = (f"select calorie_value , fats, proteins, carbohydrates "
                           f"from products "
                           f"where product_name = %s")
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (pram,))
                data = await cursor.fetchone()
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def add_count_calories(self, args: List, user: str):
        try:
            calorie, protein, fat, carbohydrate = 0, 0, 0, 0
            temporary = []
            food_list = list(args)
            key_value_pairs = [pair.strip() for pair in food_list[-1].split(',')]
            food_dict = {i.split("-")[0].strip(): i.split("-")[1].strip() for i in key_value_pairs}

            for key, value in food_dict.items():
                r = await self.func(key)
                calorie += calorie_calculation(r[0], value)
                protein += calorie_calculation(r[2], value)
                fat += calorie_calculation(r[1], value)
                carbohydrate += calorie_calculation(r[-1], value)
            temporary.append(int(calorie)), temporary.append(protein)
            temporary.append(ceil(fat)), temporary.append(ceil(carbohydrate))
            food_list.extend(temporary)
            food_list.append(user)

            sql_command = ("""INSERT INTO nutrition_info(nutrition_day, nutrition_info, calorie, proteins, fats, 
                              carbohydrates, users) VALUES (%s, %s, %s, %s, %s, %s, %s)""")

            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, food_list)
            self.__mydb.commit()
            return food_list
        except aiomysql.Error as exc:
            logging.error(f"{exc}")
        except BaseException as exc:
            logging.error(f"{exc}")

    async def sports_exercises(self):
        try:
            sql_command = """SELECT exercise, approaches FROM sports_exercises"""

            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command)
                data = await cursor.fetchall()
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def add_time_my_workout(self, workout_time: str, username: str):
        try:
            sql_command = """INSERT INTO time_my_workout (workout_time, users)
                             VALUES (%s, %s)"""

            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (workout_time, username))
            self.__mydb.commit()
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def food_information(self, product_category_id):
        """Таблица удалена нужно востановить"""
        try:
            sql_command = (
                "select products_name, calorie_value, proteins, fats, carbohydrates "
                "from products1 "
                "where products_category_id = %s"
            )

            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (product_category_id,))
                data = await cursor.fetchall()
                # print(exercise)
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def food_index(self, product_name):
        try:
            sql_command = (
                "select products_category_id "
                "from products1 "
                "where products_name = %s"
            )
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (product_name,))
                exercise = await cursor.fetchone()
                data = list(exercise)
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def sports_muscles(self):
        """Переробіть"""
        try:
            sql_command = """SELECT muscl FROM muscles"""

            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command)
                data = await cursor.fetchall()
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def workout_day(self, call_initial: str) -> List[tuple]:
        try:
            sql_command = """
                SELECT DISTINCT day_workout, day_workout_en
                FROM training_programmes_from_athletes tpfa
                JOIN athletes ath ON tpfa.athlete_id = ath.athlete_id
                JOIN day_workout_athletes dy ON tpfa.day_workout_id = dy.day_workout_id
                WHERE ath.call_initial = %s
            """

            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (call_initial,))
                data = await cursor.fetchall()
                print(data)
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def muscle_class(self, call_initial, call_day_workout) -> List[tuple]:
        try:
            sql_command = """
                SELECT DISTINCT muscl
                FROM training_programmes_from_athletes tpfa
                JOIN athletes ath ON tpfa.athlete_id = ath.athlete_id
                JOIN day_workout_athletes dy ON tpfa.day_workout_id = dy.day_workout_id
                JOIN muscles m ON tpfa.muscl_id = m.muscl_id
                WHERE ath.call_initial = %s and dy.day_workout_en = %s
            """

            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (call_initial, call_day_workout,))
                data = await cursor.fetchall()
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def workout_exercises(self, call_initial, call_day_workout, call_muscle) -> List[tuple]:
        try:
            sql_command = """
                SELECT se.exercise_photo, se.exercise, tpfa.approaches, tpfa.repetition, se.link
                FROM training_programmes_from_athletes tpfa
                JOIN athletes ath ON tpfa.athlete_id = ath.athlete_id
                JOIN day_workout_athletes dy ON tpfa.day_workout_id = dy.day_workout_id
                JOIN muscles m ON tpfa.muscl_id = m.muscl_id
                JOIN sports_exercises se on se.exercise_id = tpfa.exercise_id
                WHERE ath.call_initial = %s and dy.day_workout_en = %s and m.muscl = %s
            """
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (call_initial, call_day_workout, call_muscle, ))
                data = await cursor.fetchall()
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def sports_trein(self, muscl_id):
        try:
            sql_command = """select exercise, link from sports_exercises where muscl_id = %s"""

            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (muscl_id,))
                data = await cursor.fetchall()
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def muscle_group_inline(self):
        try:
            sql_command = """select muscl, call_muscl from muscles"""

            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command)
                data = await cursor.fetchall()
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def additives_inline(self):
        try:
            sql_command = """select additives_group_name, additives_groups_call from additives_groups"""

            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command)
                data = await cursor.fetchall()
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def additives_groups_inline(self, addit_groups_call):
        try:
            sql_command = """
                SELECT additives_groups_txt, link
                FROM additives_groups
                WHERE additives_groups_call = %s
            """

            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (addit_groups_call,))
                data = await cursor.fetchall()
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def additives_groups_inline2(self, addit_groups_call):
        try:
            sql_command = """
                SELECT an.additive_name, an.additive_name_call, ag.additives_groups_txt, ag.link
                FROM additive_names an
                JOIN additives_groups ag
                ON an.additives_group_id = ag.additives_group_id
                WHERE ag.additives_groups_call = %s
            """

            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (addit_groups_call,))
                data = await cursor.fetchall()
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def callback_for_additives_subgroup(self, addit_groups_call: str):
        try:
            sql_command = """
                SELECT ag.additives_groups_call, an.additive_name_txt 
                FROM additive_names an
                JOIN additives_groups ag 
                ON an.additives_group_id = ag.additives_group_id
                WHERE an.additive_name_call = %s
            """
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (addit_groups_call,))
                data = await cursor.fetchone()
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def training_at_home_day(self, training_call: str) -> List[tuple]:
        try:
            sql_command = """
                SELECT distinct training_day, training_day_call 
                FROM fitnesdb.training_at_home
                WHERE title_call = %s
            """
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (training_call,))
                data = await cursor.fetchall()
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def training_at_home(self, training_call: str):
        try:
            sql_command = """
                SELECT tah.description, se.link, se.exercise, tah.sets, 
                       tah.reps, tah.rest, tah.training_day, tah.title_call
                FROM training_at_home tah
                JOIN sports_exercises se ON tah.exercise_id = se.exercise_id
                WHERE tah.training_day_call = %s
            """
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (training_call,))
                data = await cursor.fetchall()
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def check_if_the_user_has_any_training(self, tg_id: int):
        """
            Перевіляє чи є вже тренування у користувача 0/1...n
        """
        try:
            sql_command = """
                SELECT count(uw.user_id) 
                FROM user_workout uw
                join users us on uw.user_id = us.user_id
                where us.telegram_id = %s
            """
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (tg_id,))
                data = await cursor.fetchone()
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def my_workout_day(self) -> List[tuple]:
        """
            повертає день тренування та callback_data на день тренування
            для функції create_my_workout
        """
        try:
            sql_command = """
                SELECT day_of_the_week, day_of_the_week_call 
                FROM fitnesdb.workout_day
            """
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command)
                data = await cursor.fetchall()
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def my_sports_exercises_in_training(self, muscle_id: int) -> List[tuple]:
        try:
            sql_command = """
                SELECT exercise_photo, exercise
                FROM sports_exercises
                WHERE muscl_id = %s
            """
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (muscle_id,))
                data = await cursor.fetchall()
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def check_telegram_id(self, telegram_id: int) -> int:
        try:
            sql_command = """
                SELECT user_id
                FROM users
                WHERE telegram_id = %s
            """
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (telegram_id,))
                data = await cursor.fetchone()
                data = int(data[0])
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def check_sporting_exercise_id(self, sporting_exercise: str) -> int:
        try:
            sql_command = """
                SELECT exercise_id
                FROM sports_exercises
                WHERE exercise = %s
            """
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (sporting_exercise,))
                data = await cursor.fetchone()
                data = int(data[0])
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def add_an_exercise_to_my_workout_routine(self,
                                                    user_id: int,
                                                    workout_day: int,
                                                    muscle_group: int,
                                                    sporting_exercise_id: int) -> None:
        try:
            sql_command = """
                INSERT INTO user_workout (workout_day_id, exercise_id, muscl_id, user_id)
                VALUES (%s, %s, %s, %s)
            """
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (workout_day, sporting_exercise_id, muscle_group, user_id))
                await self.__mydb.commit()
        except aiomysql.Error as exc:
            logging.error(f"{exc}")
