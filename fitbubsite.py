
from flask import Flask, render_template, redirect, flash, session, request
import jinja2

app = Flask(__name__)

# A secret key is needed to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined



@app.route("/add_exercise", methods=["POST"])
def index():
    """Return add exercise from."""

    return render_template("add_exercise.html")


if __name__ == "__main__":
    app.run(debug=True, port=3000, host='0.0.0.0')