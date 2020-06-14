
from flask import Flask, render_template, redirect, flash, session, request, jsonify
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
	"""Show add_exercise view as landing page, may change this"""
	if request.form and session.get('user'):
		add_exercise()
		return redirect("/add_exercise")
	else:
		flash('Please log in')
		return render_template("add_exercise.html")

@app.route("/register", methods=["GET", "POST"])
def registration():
	"""Show registration form"""
	if request.form:
		email = request.form['email']
		password = request.form['password']
		confirm_password = request.form['confirm-password']
		user_exists = User.query.filter_by(email = email).\
						  one_or_none()
		if user_exists:
			flash('Email already used, TODO need to handle\
				   forgotten password')
			return render_template("registration.html") 
		elif password == confirm_password:
			new_user = User(email=email, password=password)
			db.session.add(new_user)
			db.session.commit()
			flash('Registered! Let\'s get exercisin\'!!\n Please log in!')
			return redirect("/login")
		else:
			flash('Passwords do not match, please try again')
			return render_template("registration.html") 
	return render_template("registration.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	"""Return login form and allow user to login using 
	   username/password credentials, passwords not hashed yet!"""
	if request.form:
		email = request.form['email']
		password = request.form['password']
		user = User.query.filter_by(email = email).one_or_none()
		if user:
			if password == user.password:
				session['user'] = user.user_id
				flash('Success, you are now free to log your EXERCISES!\n \
					   Keep calm and exercise on!')
				return redirect("/add_exercise")
			else:
				flash('incorrect email or password.')
				return redirect("/login")

		else: 
			flash('incorrect email or password, try again buddy!')
			return redirect("/login")

	else:
		return render_template("login.html")

@app.route("/logout")
def logout():
	"""Log user out of site
	Find user in session, remove user from session using pop() function 
	"""
	session.pop('user')
	return redirect("/login")


@app.route("/add_exercise", methods=["GET", "POST"])
def add_exercise_form():
	"""Return add exercise form"""
	if request.form:
		if session.get('user'):
			add_exercise()
			return redirect("/add_exercise")
		else:
			flash('Please Login Sir or Ma\'am')
			return redirect("/login")
	else:
		return render_template("add_exercise.html")

def add_exercise():
	"""addition of exercises to DB!, current user is hardcoded
	will change to user in session once it actually functions"""
	user_id = session.get('user')
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
	user_id = session.get('user')
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
	else:
		flash('Please login')
		return redirect("/login")





if __name__ == "__main__":

	connect_to_db(app)
	app.run(debug=True, port=3000, host='0.0.0.0')
