import asyncio
import json
import logging

from typing import List
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
                raise

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

    async def add_user_information_about_nutrition(self,
                                                   nutrition_day: str,
                                                   nutrition_info: str,
                                                   calorie: str,
                                                   proteins: str,
                                                   fats: str,
                                                   carbohydrates: str,
                                                   telegram_id: int):
        try:
            sql_command = ("""INSERT INTO nutrition_user_info(nutrition_day, nutrition_info, calorie, proteins, fats, 
                              carbohydrates, telegram_id) VALUES (%s, %s, %s, %s, %s, %s, %s)""")

            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (nutrition_day, nutrition_info, calorie, proteins, fats,
                                                   carbohydrates, telegram_id))
            await self.__mydb.commit()
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

    async def add_time_my_workout(self, time_workout: str, telegra_id: int):
        try:
            sql_command = """INSERT INTO time_my_workout (telegra_id, time_workout)
                             VALUES (%s, %s)"""

            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (telegra_id, time_workout))
                await self.__mydb.commit()
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def training_time_in_the_last_7_days(self, telegram_id: int):
        try:
            sql_command = """
                SELECT time_workout 
                FROM time_my_workout
                WHERE DATE_FORMAT(addition_time, 'Y-m-d') >= DATE_FORMAT(DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 7 DAY), 
                'Y-m-d')
                AND DATE_FORMAT(addition_time, 'Y-m-d') <= DATE_FORMAT(CURRENT_TIMESTAMP, 'Y-m-d')
                AND telegra_id = %s
            """
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (telegram_id,))
                data = [j for i in await cursor.fetchall() for j in i]
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def training_time_in_the_last_month(self, telegram_id: int):
        try:
            sql_command = """
                SELECT time_workout 
                FROM time_my_workout
                WHERE DATE_FORMAT(addition_time, 'Y-m-d') >= DATE_FORMAT(DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 1 MONTH), 
                'Y-m-d')
                AND DATE_FORMAT(addition_time, 'Y-m-d') <= DATE_FORMAT(CURRENT_TIMESTAMP, 'Y-m-d')
                AND telegra_id = %s
            """
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (telegram_id,))
                data = [j for i in await cursor.fetchall() for j in i]
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def recipes_information(self) -> List[tuple]:
        try:
            sql_command = """
                SELECT recipt_id, photo_of_dish, dish_name, ingredients
                FROM recipes
            """
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command)
                data = await cursor.fetchall()
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

    async def training_at_home(self, training_call: str) -> List[tuple]:
        """
            training_at_home повертає масиз в тренуваннями для дому
        """
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

    async def my_sports_exercises_in_training(self,
                                              muscle_id: int,
                                              exercise_ids: List[int] | int) -> List[tuple]:
        """
            my_sports_exercises_in_training повертає масив з спортивними вправами по
            заданому muscle_id та exercise_ids - список id вправ які не рекомндуються робити при
            вказаних захворюваннях користуача
        """
        try:
            if exercise_ids != 0:
                exercise_ids = ','.join(map(str, exercise_ids))
            sql_command = f"""
                SELECT exercise_photo, exercise
                FROM sports_exercises
                WHERE muscl_id = %s AND exercise_id NOT IN ({exercise_ids})
            """
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (muscle_id,))
                data = await cursor.fetchall()
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def check_telegram_id(self, telegram_id: int) -> int:
        """
            check_telegram_id певертає id телеграму користувача
        """
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
        """
            check_sporting_exercise_id повертає id спортивної вправи
        """
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
        """
            add_an_exercise_to_my_workout_routine додає тренуання до заданого пористувача
        :param user_id:  id користувача
        :param workout_day: id дня тижня
        :param muscle_group: id м'язової групи
        :param sporting_exercise_id: id спортивної вправи
        """
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

    async def delete_user_workout(self, telegram_id):
        """
            delete_user_workout видаляє всі тренування у заданого користувача
        """
        try:
            sql_command = """
                DELETE us
                FROM user_workout us
                JOIN users u ON us.user_id = u.user_id
                WHERE u.telegram_id = %s
            """
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (telegram_id,))
                await self.__mydb.commit()
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def check_uses_disease(self, telegram_id: int) -> int:
        """
            check_uses_disease тримуємо кількість захворювань у заданого користувача (1/0)
        """
        try:
            sal_command = """SELECT COUNT(user_diseases_id) FROM user_diseases WHERE telegram_id = %s"""
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sal_command, (telegram_id,))
                data = await cursor.fetchall()
                data = int(data[0][0])
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def update_uses_disease(self, telegram_id: int, disease_list: dict) -> None:
        """
            update_uses_disease додаємо або оновлує захворювання користувача зберігаємо у JSON
        """
        try:
            disease_list_json = json.dumps(disease_list)
            if await self.check_uses_disease(telegram_id) == 0:
                sql_command = """INSERT INTO user_diseases (disease_list, telegram_id) VALUES (%s, %s)"""
                async with self.__mydb.cursor() as cursor:
                    await cursor.execute(sql_command, (disease_list_json, telegram_id))
                    await self.__mydb.commit()
            else:
                sql_command = """UPDATE user_diseases SET disease_list = %s WHERE telegram_id = %s"""
                async with self.__mydb.cursor() as cursor:
                    await cursor.execute(sql_command, (disease_list_json, telegram_id))
                    await self.__mydb.commit()
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def view_the_index_of_recommendations(self, telegram_id: int) -> int:
        """
            view_the_index_of_recommendations отримуємо індекс рекомандації (1'on'/0'off')
        """
        try:
            sql_command = """SELECT recommendations FROM user_diseases WHERE telegram_id = %s"""
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (telegram_id,))
                data = await cursor.fetchall()
                data = int(data[0][0])
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def update_the_recommendation_index(self, rec_index: int, telegram_id: int) -> None:
        """
            update_the_recommendation_index оновлую індекс рекомендацій (1'on'/0'off')
        """
        try:
            sql_command = """UPDATE user_diseases SET recommendations = %s WHERE telegram_id = %s"""
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (rec_index, telegram_id))
                await self.__mydb.commit()
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def music_playlists(self) -> List[tuple]:
        """
            music_playlists повертає назву плейліста та цого link
        """
        try:
            sql_command = """SELECT playlist_name, playlist_link FROM music_playlists"""
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command)
                data = await cursor.fetchall()
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def exercises_that_are_not_recommended_for_the_disease(self, telegram_id: int) -> List[tuple]:
        """
            exercises_that_are_not_recommended_for_the_disease повертає масив який містить id спортивний вправ.
            Спочатку отримуэмо JSON якия мість всі захворювання користувача,далі отримуємо id всіх спортивний вправ
            які противопоказіні по цйому захворюванню.
        """
        try:
            user_disease_json: dict
            sql_command = """SELECT disease_list FROM user_diseases WHERE telegram_id = %s"""
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (telegram_id,))
                data = await cursor.fetchone()
                user_disease_json = json.loads(data[0])

            async with self.__mydb.cursor() as cursor:
                placeholders = ','.join(['%s' for _ in user_disease_json.values()])
                sql_command = f"""
                    SELECT DISTINCT cedd.exercise_id
                    FROM fitnesdb.contraindications_exercise_due_diseases cedd
                    JOIN fitnesdb.disease d ON cedd.disease_id = d.disease_id
                    WHERE d.disease_name IN ({placeholders})
                """
                await cursor.execute(sql_command, list(user_disease_json.values()))
                data = await cursor.fetchall()
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def my_training_program_training_day(self, telegram_id: int) -> List[tuple]:
        try:
            sql_command = """
                SELECT wd.day_of_the_week, wd.day_of_the_week_call
                FROM user_workout uw
                JOIN workout_day wd ON uw.workout_day_id = wd.workout_day_id
                JOIN users u ON uw.user_id = u.user_id
                WHERE u.telegram_id = %s
                GROUP BY wd.day_of_the_week, wd.day_of_the_week_call
            """
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (telegram_id,))
                data = await cursor.fetchall()
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")

    async def my_training_programme_sport_exercise(self, telegram_id: int, call_workout_day: str) -> List[tuple]:
        try:
            sql_command = """
                SELECT se.link, se.exercise
                FROM user_workout uw
                JOIN workout_day wd ON uw.workout_day_id = wd.workout_day_id
                JOIN users u ON uw.user_id = u.user_id
                JOIN sports_exercises se ON uw.exercise_id = se.exercise_id 
                WHERE u.telegram_id = %s and wd.day_of_the_week_call = %s
            """
            async with self.__mydb.cursor() as cursor:
                await cursor.execute(sql_command, (telegram_id, call_workout_day))
                data = await cursor.fetchall()
                return data
        except aiomysql.Error as exc:
            logging.error(f"{exc}")
