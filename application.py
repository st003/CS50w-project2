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

USERS = set()
CHANNELS = {}
PRIVATES = {}


# VIEWS

# INDEX ROUTES
@app.route("/", methods=['GET', 'POST'])
def index():

    if request.method == 'GET':

        # redirect active users to last channel when starting new browser session
        # this only applies to the index page
        if session.get('last_channel') and not request.args.get('remember'):
            return redirect(url_for('channel', channel_name=session.get('last_channel')))

        return render_template('index.html', channels=CHANNELS, users=USERS)

    # http method is POST
    else:

        if not request.form.get('username'):
            return error('You must provide a username')

        username = request.form.get('username')

        if username in USERS:

            return error('Username is taken')

        else:

            USERS.add(username)
            session['username'] = username

            return redirect(url_for('index'))


# CHANNEL ROUTES
@app.route("/channel/<channel_name>", methods=['GET'])
@login_required
def channel(channel_name):

    if not channel_name:
        return error('No channel name selected')
    
    if channel_name not in CHANNELS:
        return redirect(url_for('index'))
    
    # store last visited channel in the user's session 
    session['last_channel'] = channel_name

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
    
    return redirect(url_for('index', remember=False))


@app.route("/private_channel/<other_user>", methods=['GET'])
@login_required
def private_channel(other_user):

    if not other_user:
        return error('No other user was provided')
    
    users = frozenset([other_user, session['username']])

    if users not in PRIVATES:
        PRIVATES[users] = deque(maxlen=100)

    return render_template(
        'private_channel.html',
        other_user=other_user,
        messages=PRIVATES[users],
        channel_hash=hash(users)
    )


# WEB SOCKETS
@socketio.on('submit public message')
def save_public_message(data):

    public_message = {
        'username': session['username'],
        'message': data['message'],
        'timestamp': datetime.now().strftime('%m-%d-%Y %M:%S')
    }

    # add latest message to channel
    CHANNELS[data['channelName']].append(public_message)

    emit(
        'broadcast public message',
        {'channelName': data['channelName'], 'publicMessage': public_message},
        broadcast=True
    )


@socketio.on('submit private message')
def save_private_message(data):

    private_message = {
        'username': session['username'],
        'message': data['message'],
        'timestamp': datetime.now().strftime('%m-%d-%Y %M:%S')
    }

    users = frozenset([data['otherUser'], session['username']])

    # add latest message to channel
    PRIVATES[users].append(private_message)

    emit(
        'broadcast private message',
        {'channelHash': hash(users), 'privateMessage': private_message},
        broadcast=True
    )