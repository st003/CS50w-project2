from flask import render_template


def error(error_message):
	"""
	Accepts a single string arguement which is a developer
	defined error message. Sends the user to the error page 
	and renders the error message.
	"""
	return render_template('error.html', error_message=error_message)