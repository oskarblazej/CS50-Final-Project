import sys

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from decorators import login_required, format_time

# Configure application
app = Flask(__name__)
# Filter needed to format number of seconds to time presented as HH:MM:SS in jinja
app.jinja_env.filters["format_time"] = format_time
# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure database using CS50's Library - allowed by cs50 stuff on reddit
db = SQL("sqlite:///database.db")



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/')
@login_required
def index():
    """Handle main website"""
    if not session['user_id']:
        return redirect('/auth/login')
    tasks = db.execute('SELECT * FROM tasks WHERE user_id = ?', session["user_id"])
    return render_template('manage_tasks.html', tasks=tasks)


@app.route('/auth/register', methods=["POST", "GET"])
def register():
    """Register new user into database"""
    session.clear()
    if request.method == "POST":
        # Even when all of these fields are required in the template we need to check if user provided neccessary
        # Information in case he changed something in the code

        listing = [item["email"] for item in db.execute("SELECT email FROM users")]

        if not request.form.get("email"):
            return render_template("error_handling.html", message="Please enter email")
        elif not request.form.get("password"):
            return render_template("error_handling.html", message="Please enter password")
        elif not request.form.get("confirm_pass"):
            return render_template("error_handling.html", message="Please confirm password")

        # Check if email is valid
        if '@' not in request.form.get("email"):
            return render_template("error_handling.html", message="Please enter valid email")
        # Check if email is in db already
        if request.form.get("email") in listing:
            return render_template("error_handling.html", message="Email already linked to existing account")



        email = request.form.get("email")
        password = request.form.get("password")

        if password != request.form.get("confirm_pass"):
            return render_template("error_handling.html", message="Passwords do not match")

        db.execute("INSERT INTO users (email, password) VALUES (?, ?)", email, generate_password_hash(password))

        return redirect('/auth/login')
    else:
        return render_template('auth/register.html')



@app.route('/auth/login', methods=["GET", "POST"])
def login():
    """ Login in registered user"""
    session.clear()
    if request.method == "POST":
        if not request.form.get("email"):
            return render_template("error_handling.html", message="Please enter email")
        if not request.form.get("password"):
            return render_template("error_handling.html", message="Please enter password")

        email = request.form.get("email")
        password = request.form.get("password")
        line = db.execute("SELECT * FROM users WHERE email = ?", email)

        # If there are no results user entered wrong email, we also need to check for password
        if len(line) != 1 or not check_password_hash(line[0]["password"], password):
            return render_template("error_handling.html", message="Bad email or password")

        session["user_id"] = line[0]["id"]

        return redirect('/')
    else:
        return render_template('auth/login.html')



@app.route('/add/', methods=["POST"])
@login_required
def add_task():
    if request.method == "POST":
        name = request.form.get('taskname')
        if not name:
            return render_template("error_handling.html", message="Please enter task name")
        db.execute("INSERT INTO tasks (name, user_id) VALUES (?, ?)", name, session["user_id"])
        return redirect('/')

@app.route('/change/', methods=["POST"])
@login_required
def change_task():
    if request.method == "POST":
        if not 'task_id' in request.form:
                return render_template("error_handling.html", message="No task to be changed")
        if request.form["submit_button"] == "Edit":
            newname = request.form.get('editName')
            if not newname:
                return render_template("error_handling.html", message="Please enter task name")
            db.execute("UPDATE tasks SET name = ? WHERE task_id = ? AND user_id = ?",newname, request.form['task_id'],session["user_id"])
            return redirect('/')
        elif request.form["submit_button"] == "Remove":
            db.execute("DELETE FROM tasks WHERE task_id = ? AND user_id = ?", request.form['task_id'], session["user_id"])
            return redirect('/')

@app.route('/timer', methods=["POST"])
@login_required
def timer():
    if request.method == "POST":
        request_data = request.get_json()
        time = request_data.get('time')
        task_id = request_data.get('task_id')

        if not time:
            return render_template("error_handling.html", message="Could not charge time")
        # Get current time before updating
        current = db.execute("SELECT charged FROM tasks WHERE task_id = ? AND user_id = ?",task_id, session["user_id"])[0]["charged"]
        db.execute("UPDATE tasks SET charged = ? WHERE task_id = ? AND user_id = ?", current+time, task_id,session["user_id"])
        return redirect('/')

@app.route('/auth/logout')
@login_required
def logout():
    session.clear()
    return redirect('/')