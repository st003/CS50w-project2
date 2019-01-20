import os

from flask import Flask, redirect, render_template, request, session, url_for
from flask_socketio import SocketIO, emit

from helpers import error

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# GLOBALS

USERNAMES = set()

# VIEWS

# INDEX ROUTES
@app.route("/", methods=['GET', 'POST'])
def index():

    if request.method == 'GET':

        return render_template('index.html')

    # http method is POST
    else:

        if not request.form.get('username'):
            return error('You must provide a username')

        username = request.form.get('username')

        if username in USERNAMES:

            return error('Username is taken')

        else:

            USERNAMES.add(username)
            session['username'] = username

            return redirect(url_for('index'))