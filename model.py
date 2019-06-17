"""Models and database functions for fitbub db"""

from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime 

db = SQLAlchemy()

class User(db.Model):
	"""User model. A user can have many exercise entries."""

	__tablename__ = 'users'

	user_id = db.Column(db.Integer, 
						primary_key=True,
						autoincrement=True
						)
	email = db.Column(db.String(100),
					  unique=True, 
					  nullable=False
					  )
	password = db.Column(db.String(50), 
						 nullable=False)
	exercises = db.relationship('Exercise', 
								 backref='users', 
								 lazy=True
								 )
	entries = db.relationship('ExerciseEntry', 
								backref='user',
								lazy = True 
								)

	def __repr__(self):
		"""show user information"""
		return "<User id={} email={}>".format(
			self.user_id, self.email)


class Exercise(db.Model):
	"""exercise model. exercises will have one user."""

	__tablename__ = 'exercises'

	exercise_id = db.Column(db.Integer,
							primary_key=True,
							autoincrement=True
							)
	user_id = db.Column(db.Integer, 
						db.ForeignKey('users.user_id'),
						nullable=False,
						)
	name = db.Column(db.String(50), nullable=False)

	muscle_group = db.Column(db.String(50))

	exercise_entries = db.relationship('ExerciseEntry', 
										backref='exercises',
										lazy = True 
										)
	def __repr__(self):
		"""show exercise information"""
		return "<Exercise id={} user_id={} exercise_name={} muscle_group={}>".format(
					self.exercise_id, self.user_id, self.exercise_name, self.muscle_group)




class ExerciseEntry(db.Model):
	"""excercise entry model."""

	__tablename__ = 'exercise_entries'

	entry_id = db.Column(db.Integer,
						 primary_key=True,
						 autoincrement=True
						 )
	datetime = db.Column(db.DateTime,
						 nullable=False,
						 default=datetime.utcnow
						 )
	user_id = db.Column(db.Integer,
						db.ForeignKey('users.user_id'), 
						nullable=False
						)
	exercise_id = db.Column(db.Integer,
							db.ForeignKey('exercises.exercise_id'),
							nullable=False
							)
	num_reps = db.Column(db.Integer, nullable=False)
	weight = db.Column(db.Integer, nullable=False)




	def __repr__(self):
			"""show exercise entry information"""
			return "<ExerciseEntry id={} timestamp={} user_id={} exercise_id={} num_reps={} weight={}>".format(
					self.entry_id, self.datetime, self.user_id, self.exercise_id, self.num_reps, self.weight)
	

	#########
	#helper functions

def init_app():
	""" Flask app to connect to Flask-SQLAlchemy"""
	from flask import Flask
	app = Flask(__name__)

	connect_to_db(app)
	print("Yo, connected to DeeBee!")


def connect_to_db(app):
	""" connect to db to Flask app"""
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///exercises'
	app.config['SQLALCHEMY_ECHO'] = False
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.app = app
	db.init_app(app)


if __name__ == "__main__":

	init_app()
