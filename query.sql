SELECT se.exercise_photo, se.exercise, tpfa.approaches, tpfa.repetition, se.link
FROM training_programmes_from_athletes tpfa
JOIN athletes ath ON tpfa.athlete_id = ath.athlete_id
JOIN day_workout dy ON tpfa.day_workout_id = dy.day_workout_id
JOIN muscles m ON tpfa.muscl_id = m.muscl_id
JOIN sports_exercises se on se.exercise_id = tpfa.exercise_id
WHERE ath.call_initial = 'ar1' and dy.day_workout_en = 'mondaytothursday' and m.muscl = 'Гриди';


SELECT DISTINCT muscl
FROM training_programmes_from_athletes tpfa
JOIN athletes ath ON tpfa.athlete_id = ath.athlete_id
JOIN day_workout dy ON tpfa.day_workout_id = dy.day_workout_id
JOIN muscles m ON tpfa.muscl_id = m.muscl_id
WHERE ath.call_initial = 'ar1' and dy.day_workout_en = 'mondaytothursday';

SELECT DISTINCT day_workout, day_workout_en
FROM training_programmes_from_athletes tpfa
JOIN athletes ath ON tpfa.athlete_id = ath.athlete_id
JOIN day_workout dy ON tpfa.day_workout_id = dy.day_workout_id
WHERE ath.call_initial = 'ar1';


SELECT exercise_photo, exercise
FROM sports_exercises
WHERE muscl_id = 1;