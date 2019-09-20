
from flask import Flask, render_template, redirect, flash, session, request, jsonify
import jinja2
from model import User, Exercise, ExerciseEntry, db, connect_to_db
import json

app = Flask(__name__)

# A secret key is needed to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/login", methods=["GET", "POST"])
def login():
	"""Return login form and allow user to login credentials"""
	if request.form:
		process_login()
	else:
		return render_template("login.html")


def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # The logic here should be something like:
    #
    # - get user-provided name and password from request.form
    # - use customers.get_by_email() to retrieve corresponding Customer
    #   object (if any)
    # - if a Customer with that email was found, check the provided password
    #   against the stored one
    # - if they match, store the user's email in the session, flash a success
    #   message and redirect the user to the "/melons" route
    # - if they don't, flash a failure message and redirect back to "/login"
    # - do the same if a Customer with that email doesn't exist
    email = request.form['email']
    password = request.form['password']
    customer = User.query.filter_by(email = email).one_or_none()
    print(customer)
    if customer:
        if email == customer.email:
            if password == customer.password:
                session['user'] = email
                flash('Success, you are now free to log your EXERCISES!\n \
                       Keep calm and exercise on!')
                return redirect("/add_exercise")
            else: 
                flash('incorrect email or password, try again buddy!')
                return redirect("/login")
    
    else:
        flash('incorrect email or password.')
        return redirect("/login")

@app.route("/", methods=["GET", "POST"])
def index():
	"""Return Home Page """
	if request.form:
		add_exercise()
		return redirect("/add_exercise")
	else:
		return render_template("add_exercise.html")

@app.route("/add_exercise", methods=["GET", "POST"])
def add_exercise_from():
	"""Return add exercise form"""
	if request.form:
		add_exercise()
		return redirect("/add_exercise")
	else:
		return render_template("add_exercise.html")

def add_exercise():
	"""addition of exercises to DB!, current user is hardcoded
	will change to user in session once it actually functions"""
	user_id = 2
	exercise_name = request.form["exercise_name"]
	weight = request.form["weight"]
	num_reps = request.form["num_reps"]
	new_entry = None
	new_exercise = None

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
	flash("Exercise Logged! Don't Stop Rockin!")
	return "Exercise logged!", 200

@app.route("/exercise_history", methods=["GET", "POST"])
def exercise_history():
	"""if exercises have been logged, show them in a table"""
	user_id = 2
	if user_id:
		user_entries = db.session.query(ExerciseEntry).\
						join(Exercise).\
						filter_by(user_id = user_id).all()	
		exercise_dict = {}
		for exercise in user_entries:
			date = exercise.datetime.strftime("%b %d %Y")
			if date in exercise_dict:
				exercise_on_date = exercise_dict[date]
				exercise_on_date.append(
					{'exercise': exercise.exercises.name,
					 'weight': exercise.weight,
					 'reps': exercise.num_reps

					})
				exercise_dict[date] = exercise_on_date
			else:
				exercise_dict[date] =\
				[{'exercise': exercise.exercises.name,
				  'weight': exercise.weight,
				  'reps': exercise.num_reps
				}]		
	return render_template("exercise_history.html", exercises=exercise_dict)




if __name__ == "__main__":

	connect_to_db(app)
	app.run(debug=True, port=3000, host='0.0.0.0')
