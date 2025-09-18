from db import db
from sqlalchemy.orm import validates


class Exercise(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)

    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')
    workouts = db.relationship('Workout', secondary='workout_exercises', back_populates='exercises', viewonly=True)

    # Validations
    @validates('name', 'category', 'equipment_needed')
    def validate_not_empty(self, key, value):
        if key == 'equipment_needed':
            if not isinstance(value, bool):
                raise ValueError(f"{key} must be a boolean")
        else:
            if not value or not value.strip():
                raise ValueError(f"{key} cannot be empty")
        return value


class Workout(db.Model):
    __tablename__ = 'workouts'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')
    exercises = db.relationship('Exercise', secondary='workout_exercises', back_populates='workouts', viewonly=True)

    # Validations
    @validates('date')
    def validate_date(self, key, value):
        from datetime import date
        if not isinstance(value, date):
            raise ValueError("date must be a datetime.date object")
        return value

    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if value <= 0:
            raise ValueError("duration_minutes must be greater than 0")
        return value


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer, nullable=True)
    sets = db.Column(db.Integer, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)

    # Table Constraints
    __table_args__ = (
        db.UniqueConstraint('workout_id', 'exercise_id', name='uix_workout_exercise'),
        db.CheckConstraint("sets>0", name="check_sets_positive"),
        db.CheckConstraint("reps>0", name="check_reps_positive"),
    )

    # Relationships
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    def to_dict(self):
        return {
            'id': self.id,
            'workout_id': self.workout_id,
            'exercise_id': self.exercise_id,
            'reps': self.reps,
            'sets': self.sets,
            'duration_seconds': self.duration_seconds,
        }



