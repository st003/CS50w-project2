import os

from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_socketio import SocketIO, emit

from helpers import error, login_required

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# GLOBALS

USERNAMES = set()
CHANNELS = {}

# VIEWS

# INDEX ROUTES
@app.route("/", methods=['GET', 'POST'])
def index():

    if request.method == 'GET':

        return render_template('index.html', channels=CHANNELS)

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


# CHANNEL ROUTES
@app.route("/channel/put", methods=['POST'])
@login_required
def put_channel():

    if not request.form.get('channelName'):
        return error('Channel name not provided')

    new_channel = request.form.get('channelName')
    
    if new_channel in CHANNELS:
        return error('A channel by that name already exists')
    
    CHANNELS[new_channel] = []
    
    return redirect(url_for('index'))