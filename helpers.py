from functools import wraps
from flask import redirect, render_template, session, url_for


def login_required(f):
    """
    Checks for an active session before rendering a page.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


def error(error_message):
	"""
	Accepts a single string arguement which is a developer
	defined error message. Sends the user to the error page 
	and renders the error message.
	"""
	return render_template('error.html', error_message=error_message)