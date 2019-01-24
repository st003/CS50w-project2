import os
from datetime import datetime
from collections import deque

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
@app.route("/channel/<channel_name>", methods=['GET'])
@login_required
def channel(channel_name):

    if not channel_name:
        return error('No channel name selected')

    messages = CHANNELS[channel_name]
    
    return render_template('channel.html', channel_name=channel_name, messages=messages)


@app.route("/channel/put", methods=['POST'])
@login_required
def put_channel():

    if not request.form.get('channelName'):
        return error('Channel name not provided')

    new_channel = request.form.get('channelName')
    
    if new_channel in CHANNELS:
        return error('A channel by that name already exists')
    
    CHANNELS[new_channel] = deque(maxlen=100)
    
    return redirect(url_for('index'))


# MESSAGE ROUTES
@app.route("/messages/post", methods=['POST'])
@login_required
def post_messages():

    try:

        if not request.form.get('channelName'):
            raise ValueError('No channel name was provided')
        if not request.form.get('message'):
            raise ValueError('No message content was provided')

        message = {
            'username': session['username'],
            'message': request.form.get('message'),
            'timestamp': datetime.now()
        }

        CHANNELS[request.form.get('channelName')].append(message)
    
        return jsonify({
            'result': True,
            'message': 'Message posted successfully'
        })
    
    except Exception as error_message:

        return jsonify({
            'result': False,
            'message': f'{error_message}'
        })