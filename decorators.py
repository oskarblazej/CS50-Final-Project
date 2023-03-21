from flask import redirect, session
import math
from functools import wraps


def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/auth/login")
        return f(*args, **kwargs)
    return decorated_function


def format_time(value):
    seconds = math.floor((value) % 60);
    minutes = math.floor((value / (60)) % 60);
    hour = math.floor((value / (60 * 60)) % 60);
    return ("%02d:%02d:%02d" % (hour, minutes, seconds))