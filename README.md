# CS50w project2

CS50w project2 is a instant messaging web application. Users may resgister username, browse channels, and submit messages, both public and private. The application is built with the flask web framework and relies on web sockets and javascript for realtime communication.

For my personal touch, I implemented private messaging functionality. Users may submit private messages to any other user in the system by selecting their name from the user table on the home screen. The private channel view functions much in the same way as public channels, but messages are keep isolated between the two users.

## Description of Contents

* *static/* - Directory contains the application styles and javascript files
* *templates/* - Directory contains jinja2 templates for Flask views

* *application.py* - Contains the Flask application configuration settings, routing functions, and server side web socket listeners.
* *helpers.py* - Contains helpers functions for use in various parts of the application.
* *README.md* - This document. The thing you are literally reading right now.
* *requirements.txt* - List of application dependencies used by Pip.

## Built With

* [Python](https://www.python.org/) - Language interpreter
* [flask](http://flask.pocoo.org/) - Web framework
* [Flask-SocketIO](https://flask-socketio.readthedocs.io) - Flask web socket extention
* [Bootstrap](https://getbootstrap.com) - CSS Library
* [socket.io](https://socket.io/) - JavaScript web socket library
* [handlebars.js](https://handlebarsjs.com/) - JavaScript HTML templating library

## Authors

* **CS50w Team** - *Project outline*
* **st003** - *Initial work*