
from flask import Flask, render_template, redirect, flash, session, request
import jinja2
from model import User, Exercise, ExerciseEntry, db, connect_to_db


app = Flask(__name__)

# A secret key is needed to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/", methods=["GET", "POST"])
def index():
	"""Return Home Page """
	if request.form:
		add_exercise()
		return redirect("/add_exercise")
	else:
		return render_template("add_exercise.html")

@app.route("/add_exercise", methods=["GET", "POST"])
def add_exercise():
	"""Return add exercise form and addition of exercises!"""
	if request.form:
		user_id = 1
		exercise_name = request.form["exercise_name"]
		weight = request.form["weight"]
		num_reps = request.form["reps"]
		
		check_exercise = Exercise.query.filter_by(user_id = user_id,\
												name = exercise_name).\
												one_or_none()
		if check_exercise == None:
			new_exercise = Exercise(user_id = user_id,
									name = exercise_name
									)
			db.session.add(new_exercise)
			db.session.commit()
			check_exercise = Exercise.query.filter_by(user_id = user_id,\
												name = exercise_name).\
												one_or_none()

		new_entry = ExerciseEntry(user_id = user_id, 
								  exercise_id = check_exercise.exercise_id,
								  num_reps = num_reps,
								  weight = weight)

		db.session.add(new_entry)
		db.session.commit()
		return "Exercise logged!", 200
	else:
		return render_template("add_exercise.html")



if __name__ == "__main__":

	connect_to_db(app)
	app.run(debug=True, port=3000, host='0.0.0.0')
