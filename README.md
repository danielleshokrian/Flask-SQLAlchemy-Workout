# Flask-SQLAlchemy-Workout

# Workout Tracker API

## Project Description
Workout Tracker is a Flask-based RESTful API that allows users to manage workouts and exercises. Users can create workouts, add exercises, track sets/reps/duration, and view the relationships between workouts and exercises.

## Installation Instructions
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd Flask-SQLAlchemy-Workout/server


2. Create a virtual environment (using pipenv):

pipenv install
pipenv shell


3. Install dependencies:

pipenv install

4. Set up the database:

flask db init
flask db migrate -m "Initial migration"
flask db upgrade


5. Seed the database with sample data:

python seed.py


## Run Instructions

Run the API server locally:

python main.py

The server will run at http://127.0.0.1:5555.

## API Endpoints
### Workouts

GET /workouts
List all workouts with associated exercises.

GET /workouts/<id>
Show a single workout and its exercises.

POST /workouts
Create a new workout. Example JSON payload:

{
  "date": "2024-01-01",
  "duration_minutes": 30,
  "notes": "Morning routine"
}


DELETE /workouts/<id>
Delete a workout (also deletes associated workout exercises).

### Exercises

GET /exercises
List all exercises.

GET /exercises/<id>
Show a single exercise and associated workouts.

POST /exercises
Create a new exercise. Example JSON payload:

{
  "name": "Push Up",
  "category": "Strength",
  "equipment_needed": false
}


DELETE /exercises/<id>
Delete an exercise (also deletes associated workout exercises).

### Workout Exercises

POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
Add an exercise to a workout. Example JSON payload:

{
  "sets": 3,
  "reps": 12,
  "duration_seconds": 60
}

## Notes

Dates must be valid Python date objects (YYYY-MM-DD).

Schema validations prevent invalid data (e.g., empty strings, negative reps/sets).

Rerun python seed.py anytime to reset the database with sample data.


---

### `Pipfile`
```toml
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[dev-packages]

[packages]
flask = "*"
flask_sqlalchemy = "*"
flask_migrate = "*"
marshmallow = "*"