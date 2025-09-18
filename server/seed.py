#!/usr/bin/env python3
from datetime import date
from main import app, db
from models import Workout, Exercise, WorkoutExercise

with app.app_context():
    print("Seeding database...")

    # Clear existing data
    db.drop_all()
    db.create_all()

    # Create sample exercises
    push_up = Exercise(name="Push Up", category="Strength", equipment_needed=False)
    squat = Exercise(name="Squat", category="Strength", equipment_needed=False)
    plank = Exercise(name="Plank", category="Core", equipment_needed=False)

    # Create sample workouts
    morning_workout = Workout(date=date(2024, 1, 1), duration_minutes=30, notes="Morning routine")
    evening_workout = Workout(date=date(2024, 1, 2), duration_minutes=45, notes="Evening routine")

    db.session.add_all([push_up, squat, plank, morning_workout, evening_workout])
    db.session.commit()

    # Link exercises to workouts via WorkoutExercise
    we1 = WorkoutExercise(workout_id=morning_workout.id, exercise_id=push_up.id, sets=3, reps=12)
    we2 = WorkoutExercise(workout_id=morning_workout.id, exercise_id=squat.id, sets=3, reps=15)
    we3 = WorkoutExercise(workout_id=evening_workout.id, exercise_id=plank.id, sets=3, duration_seconds=60)

    db.session.add_all([we1, we2, we3])
    db.session.commit()

    print("Database seeded successfully.")
