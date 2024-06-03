from pydantic import BaseModel
from datetime import time
UK_EN_ALPHABET = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ye', 'ж': 'zh', 'з': 'z',
                  'и': 'y',
                  'і': 'i', 'ї': 'yi', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
                  'с': 's',
                  'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ь': '',
                  'ю': 'yu', 'я': 'ya'
                  }
CALL_FOOD_DICT = {'fruit_dried_fruit_berrie': 1, 'herb_vegetable': 2, 'mushroom_legume': 3, 'egg': 4,
                  'fish_seafood': 5,
                  'meat_offal_poultry': 6,
                  'sausage_product_canned_meat': 7, 'dairy_product': 8, 'flour_product_cereal': 9, 'nut': 10,
                  'confectionery_sweet': 11, 'fat_margarine_oil': 12}

CALL_MUSCLE_GROUP = {'muscle1': 1, 'muscle2': 2, 'muscle3': 3, 'muscle4': 4, 'muscle5': 5, 'muscle6': 6, 'muscle7': 7,
                     'muscle8': 8, 'muscle9': 9, 'muscle10': 10}

CALL_MUSCLE_GROUP_IN_TRAINER = {'hrydy': 'Гриди', 'bitseps': 'Біцепс', 'spyna': 'Спина', 'pres': 'Прес',
                                'plechy': 'Плечи',
                                'trytseps': 'Трицепс', 'peredplichchya': 'Передпліччя', 'nohy': 'Ноги', 'ikry': 'Ікри'}

MY_WORKOUT_DAY = {
    "call_worckout_day_monday": 1, "call_worckout_day_tuesday": 2,
    "call_worckout_day_wednesday": 3, "call_worckout_day_thursday": 4,
    "call_worckout_day_friday": 5, "call_worckout_day_saturday": 6,
    "call_worckout_day_sunday": 7
}


class MuscleID:
    muscle_id: str


class TimeModel(BaseModel):
    time_value: time
