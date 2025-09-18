from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from marshmallow import ValidationError
from models import Workout, Exercise, WorkoutExercise
from schemas import WorkoutSchema, ExerciseSchema, WorkoutExerciseSchema
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
migrate = Migrate()

# Initialize db and migrate with app
db.init_app(app)
migrate.init_app(app, db)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
we_schema = WorkoutExerciseSchema()


@app.route('/')
def home():
    return "<h1>Workout Tracker API</h1>", 200


@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return workouts_schema.dump(workouts)


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    w = Workout.query.get_or_404(id)
    return workout_schema.dump(w)


@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()
    try:
        validated_data = workout_schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    w = Workout(**validated_data)
    db.session.add(w)
    db.session.commit()
    return workout_schema.dump(w), 201


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    w = Workout.query.get_or_404(id)
    for we in w.workout_exercises:
        db.session.delete(we)
    db.session.delete(w)
    db.session.commit()
    return jsonify({"message": "Workout deleted"})


@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return exercises_schema.dump(exercises)


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    e = Exercise.query.get_or_404(id)
    return exercise_schema.dump(e)


@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()
    try:
        validated_data = exercise_schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    e = Exercise(**validated_data)
    db.session.add(e)
    db.session.commit()
    return exercise_schema.dump(e), 201


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    e = Exercise.query.get_or_404(id)
    for we in e.workout_exercises:
        db.session.delete(we)
    db.session.delete(e)
    db.session.commit()
    return jsonify({"message": "Exercise deleted"})


@app.route("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises", methods=["POST"])
def add_exercise_to_workout(workout_id, exercise_id):
    w = Workout.query.get_or_404(workout_id)
    e = Exercise.query.get_or_404(exercise_id)
    data = request.get_json()
    try:
        validated_data = we_schema.load({
            "workout_id": workout_id,
            "exercise_id": exercise_id,
            "sets": data.get("sets"),
            "reps": data.get("reps")
        })
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    we = WorkoutExercise(**validated_data)
    db.session.add(we)
    db.session.commit()
    return we_schema.dump(we), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)
