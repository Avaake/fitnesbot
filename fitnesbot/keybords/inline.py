from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Мій акаунт", callback_data='my_account')
        ],
        [
            InlineKeyboardButton(text="Харчування", callback_data='nutrition_call')
        ],
        [
            InlineKeyboardButton(text="БАДи та Вітаміни", callback_data='additives_call')
        ],
        [
            InlineKeyboardButton(text="Тренування", callback_data='workouts')
        ],
        [
            InlineKeyboardButton(text="Допомога", callback_data='help_call')
        ],
    ]
)

nutrition_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Продукти", callback_data='food_list')
        ],
        [
            InlineKeyboardButton(text="Рецепти", callback_data='recipes_call')
        ],
        [
            InlineKeyboardButton(text="Головне меню", callback_data='start')
        ],
    ]
)

help_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Отримати інформацію", callback_data='get_information_help')
        ],
        [
            InlineKeyboardButton(text="Лист до техпідтримки", callback_data='letter_to_technical_support')
        ],
        [
            InlineKeyboardButton(text="Головне меню", callback_data='start')
        ],
    ]
)


category_food = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🍎🍇🍌 Фрукти, сухофрукти та ягоди', callback_data='fruit_dried_fruit_berrie'),
            InlineKeyboardButton(text="🥦🥕 Зелень і овочі", callback_data='herb_vegetable')
        ],
        [
            InlineKeyboardButton(text="🍄🌰 Гриби та бобові", callback_data='mushroom_legume'),
            InlineKeyboardButton(text="🥚 Яйця", callback_data='egg')
        ],
        [
            InlineKeyboardButton(text="🐟🦐 Риба і морепродукти", callback_data='fish_seafood'),
            InlineKeyboardButton(text="🥩🍗 М’ясо, субпродукти, птиця", callback_data='meat_offal_poultry')
        ],
        [
            InlineKeyboardButton(text="🥫 Ковбасні вироби, м’ясні консерви", callback_data='sausage_product_canned_meat' ),
            InlineKeyboardButton(text="🥛🧀 Молочні продукти", callback_data='dairy_product')
        ],
        [
            InlineKeyboardButton(text="🍞🌾 Борошняні вироби, крупи", callback_data='flour_product_cereal'),
            InlineKeyboardButton(text="🥜 Горіхи", callback_data='nut')
        ],
        [
            InlineKeyboardButton(text="🥐🎂 Кондитерські вироби, солодощі", callback_data='confectionery_sweet'),
            InlineKeyboardButton(text="🧈 Жири, маргарин, олія", callback_data='fat_margarine_oil')
        ],
        [
            InlineKeyboardButton(text='Головне Меню', callback_data='nutrition_call')
        ]
    ]
)


training_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Спортивні вправи', callback_data='fitness_menu')
        ],
        [
            InlineKeyboardButton(text='Програми тренувань від спортсменів', callback_data='training_from_athletes')
        ],
        [
            InlineKeyboardButton(text="Тренування в дома", callback_data="training_at_home")
        ],
        [
            InlineKeyboardButton(text='Головне Меню', callback_data='start')
        ]
    ]
)

training_programmes_from_athletes = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Тренування Арнольда Шварценеггера', callback_data='ar1')
        ],
        [
            InlineKeyboardButton(text='Тренування Дуейна Джонсона', callback_data='ar2')
        ],
        [
            InlineKeyboardButton(text='⬅ Назад', callback_data='workouts')
        ]
    ]
)

mein2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Гриди', callback_data='muscle1')
        ],
        [
            InlineKeyboardButton(text='Спина', callback_data='muscle2')
        ],
        [
            InlineKeyboardButton(text='Плечи', callback_data='muscle3')
        ],
        [
            InlineKeyboardButton(text='Ноги', callback_data='muscle4')
        ],
    ]
)

my_account_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Розрахуй дену калорійність 🔢🍽️', callback_data='nutrientcalculator'),
        ],
        [
            InlineKeyboardButton(text='Вибіри своЇ захворювання 😖💊', callback_data='selectiondiseases'),
        ],
        [
            InlineKeyboardButton(text='Мої тренування 💪', callback_data='my_account_workout'),
            InlineKeyboardButton(text='Плей листи 🎶', callback_data='Playlists'),
        ],
        [
            InlineKeyboardButton(text='Трекер активностей', callback_data='activity_trackers_call'),
        ],
        [
            InlineKeyboardButton(text='Головне меню', callback_data='start'),
        ]
    ]
)


training_at_home_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="15-хв. тренування на м'язи, можна робити будь-де",
                callback_data='first_training_at_home'
            )
        ],
        [
            InlineKeyboardButton(
                text="Літня фігура: 6 тижнів для спалювання жиру (жінки)",
                callback_data='second_training_at_home'
            )
        ],
        [
            InlineKeyboardButton(
                text="HIT3 Тренування вдома: 8 тижнів з нарощування м'язів",
                callback_data='third_training_at_home'
            )
        ],
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data='workouts'
            )
        ],
    ]
)

my_activity_tracker_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Час тренування 🕒🏃‍",
                                 callback_data='my_time_workout_commands')
        ],
        [
            InlineKeyboardButton(text="Прийоми Їжі",
                                 callback_data="add_meals_call")
        ],
        [
            InlineKeyboardButton(text="⬅ Назад", callback_data="my_account")
        ]
    ]
)

my_time_workout_inline_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Додати час проведеного тренування ➕⏱️💪",
                                 callback_data='add_the_time_spent_training_call')
        ],
        [
            InlineKeyboardButton(text="Переглянути статистику за остані 7 днів 📊7️⃣",
                                 callback_data="analytics_of_training_last_7_days")
        ],
        [
            InlineKeyboardButton(text="Переглянути статистику за останії місяць 📊📆",
                                 callback_data="analytics_of_training_last_month")
        ],
        [
            InlineKeyboardButton(text="⬅ Назад", callback_data="my_account")
        ]
    ]
)
