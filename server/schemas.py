from marshmallow import Schema, fields, validates, ValidationError
from models import Workout, Exercise, WorkoutExercise
from datetime import date

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    sets = fields.Int(required=True)
    reps = fields.Int(required=True)

    @validates("sets")
    def validate_sets(self, value):
        if value <= 0:
            raise ValidationError("Sets must be greater than 0")

    @validates("reps")
    def validate_reps(self, value):
        if value <= 0:
            raise ValidationError("Reps must be greater than 0")

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

    @validates("name")
    def validate_name(self, value):
        if not value.strip():
            raise ValidationError("Exercise name cannot be empty")
        
    workouts = fields.Nested(
        'WorkoutSchema', 
        many=True, 
        only=("id", "name", "workout_exercises"),
        dump_only=True
    )
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int()
    notes = fields.Str()

    @validates("name")
    def validate_name(self, value):
        if not value.strip():
            raise ValidationError("Workout name cannot be empty")
        
    exercises = fields.Nested(
        'ExerciseSchema', 
        many=True, 
        only=("id", "name"),
        dump_only=True
    )

    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)
