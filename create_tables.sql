CREATE TABLE fitnesdb.users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    telegram_id BIGINT NOT NULL UNIQUE,
    first_name VARCHAR(50) DEFAULT NULL,
    user_name VARCHAR(50) DEFAULT NULL,
    language_code VARCHAR(3) DEFAULT NULL,
    reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fitnesdb.day_workout (
    day_workout_id INT AUTO_INCREMENT PRIMARY KEY,
    day_workout VARCHAR(13),
    day_workout_en VARCHAR(30)
);

CREATE TABLE fitnesdb.muscles(
	muscl_id INT AUTO_INCREMENT PRIMARY KEY,
    muscl VARCHAR(50),
	call_muscl VARCHAR(50)
);

CREATE TABLE fitnesdb.sports_exercises (
    exercise_id INT AUTO_INCREMENT PRIMARY KEY,
    muscl_id INT NOT NULL,
	exercise_photo VARCHAR(400),
    exercise VARCHAR(100),
	link VARCHAR(400),
    FOREIGN KEY (muscl_id) REFERENCES fitnesdb.muscles(muscl_id)
);

CREATE TABLE fitnesdb.user_workout (
	user_workout_id INT AUTO_INCREMENT PRIMARY KEY,
	workout_day_id INT,
	exercise_id INT,
    muscl_id INT,
    user_id INT,
    FOREIGN KEY (workout_day_id) REFERENCES fitnesdb.workout_day(workout_day_id),
    FOREIGN KEY (exercise_id) REFERENCES fitnesdb.sports_exercises(exercise_id),
    FOREIGN KEY (muscl_id) REFERENCES fitnesdb.muscles(muscl_id),
    FOREIGN KEY (user_id) REFERENCES fitnesdb.users(user_id)
);

CREATE TABLE fitnesdb.athletes (
	athlete_id INT AUTO_INCREMENT PRIMARY KEY,
	athlete_name VARCHAR(50),
	call_initial VARCHAR(4)
);

CREATE TABLE fitnesdb.day_workout_athletes (
    day_workout_id INT AUTO_INCREMENT PRIMARY KEY,
    day_workout VARCHAR(50),
	day_workout_en VARCHAR(50)
);

CREATE TABLE fitnesdb.training_programmes_from_athletes (
	training_programmes_id INT AUTO_INCREMENT PRIMARY KEY,
    athlete_id INT,
    muscl_id INT,
    exercise_id INT,
    day_workout_id INT,
	approaches VARCHAR(255),
	repetition VARCHAR(255),
    FOREIGN KEY (muscl_id) REFERENCES fitnesdb.muscles(muscl_id),
    FOREIGN KEY (athlete_id) REFERENCES fitnesdb.athletes(athlete_id),
    FOREIGN KEY (exercise_id) REFERENCES fitnesdb.sports_exercises(exercise_id),
    FOREIGN KEY (day_workout_id) REFERENCES fitnesdb.day_workout_athletes(day_workout_id)
);

CREATE TABLE fitnesdb.user_diseases (
	user_diseases_id INT AUTO_INCREMENT PRIMARY KEY,
    disease_list JSON,
    telegram_id BIGINT,
    FOREIGN KEY (telegram_id) REFERENCES fitnesdb.users(telegram_id)
);

CREATE TABLE fitnesdb.training_at_home (
    training_at_home_id INT AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(1000),
    title VARCHAR(500),
    title_call VARCHAR(100),
    exercise_id INT,
    sets VARCHAR(10) DEFAULT '1',
    reps VARCHAR(10) DEFAULT '1',
    rest VARCHAR(20) DEFAULT 'Без відпочинку',
    training_day VARCHAR(50) DEFAULT 'Кожен день',
    training_day_call VARCHAR(50),
    FOREIGN KEY (exercise_id) REFERENCES fitnesdb.sports_exercises(exercise_id)
);

CREATE TABLE fitnesdb.time_my_workout (
	time_id INT AUTO_INCREMENT PRIMARY KEY,
    telegram_id BIGINT,
    time_workout varchar(10),
    addition_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (telegram_id) REFERENCES fitnesdb.users(telegram_id)
);

CREATE TABLE fitnesdb.disease (
	disease_id INT AUTO_INCREMENT PRIMARY KEY,
    disease_name VARCHAR(50),
    description_disease VARCHAR(1000) DEFAULT NULL,
    contraindications VARCHAR(255) DEFAULT NULL
);

CREATE TABLE fitnesdb.contraindications_exercise_due_diseases (
	contraindication_id INT AUTO_INCREMENT PRIMARY KEY,
    disease_id INT,
    exercise_id INT,
    FOREIGN KEY (disease_id) REFERENCES fitnesdb.disease(disease_id),
    FOREIGN KEY (exercise_id) REFERENCES fitnesdb.sports_exercises(exercise_id)
);

CREATE TABLE fitnesdb.products_category(
	products_category_id INT AUTO_INCREMENT PRIMARY KEY,
    products_category_name VARCHAR(100)
);

CREATE TABLE fitnesdb.products (
	product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(50),
    products_category_id INT,
	calorie VARCHAR(10),
    proteins VARCHAR(10),
    fats VARCHAR(10),
    carbohydrates VARCHAR(10),
    FOREIGN KEY (products_category_id) REFERENCES fitnesdb.products_category(products_category_id)
);

CREATE TABLE fitnesdb.nutrition_user_info (
	nutrition_id INT AUTO_INCREMENT PRIMARY KEY,
    nutrition_day VARCHAR(20),
    nutrition_info VARCHAR(600),
    calorie VARCHAR(10),
    proteins VARCHAR(10),
    fats VARCHAR(10),
    carbohydrates VARCHAR(10),
    telegram_id BIGINT,
    add_data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (telegram_id) REFERENCES fitnesdb.users(telegram_id)
);

CREATE TABLE fitnesdb.recipes (
	recipt_id INT AUTO_INCREMENT PRIMARY KEY,
    photo_of_dish VARCHAR(300),
    dish_name VARCHAR(100),
    ingredients VARCHAR(1000),
    method_of_preparation VARCHAR(3000)
);

CREATE TABLE fitnesdb.music_playlists (
	playlists_id INT AUTO_INCREMENT PRIMARY KEY,
    playlist_name VARCHAR(30),
    playlist_link VARCHAR(300)
);

CREATE TABLE fitnesdb.additives_groups(
	additives_group_id INT AUTO_INCREMENT PRIMARY KEY,
    additives_group_name VARCHAR(255),
    additives_groups_call VARCHAR(255),
    additives_groups_txt  VARCHAR(1000),
    link VARCHAR(500)
);

CREATE TABLE fitnesdb.additive_names(
	additive_name_id INT AUTO_INCREMENT PRIMARY KEY,
    additive_name VARCHAR(255),
    additive_name_call VARCHAR(255),
    additives_group_id INT,
    additive_name_txt VARCHAR(1000),
    FOREIGN KEY (additives_group_id) REFERENCES fitnesdb.additives_groups(additives_group_id)
);