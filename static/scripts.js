document.addEventListener('DOMContentLoaded', () => {

    // compile template for adding new messages
    const messageTemplate = Handlebars.compile('<div class="row message"><div class="col-10">{{ message }}</div><div class="col-2 text-right"><span class="metaData">{{ username }} - {{ timestamp }}</span></div></div>');

    // connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // add scripts for channel template
    if (document.querySelector('#publicChannel')) {

        // page globals
        const scrollPoint = document.querySelector('#scrollPoint');

        // configure websocket event listeners
        socket.on('connect', () => {

            document.querySelector('#messageForm').onsubmit = () => {

                // get form data
                const channelName = document.querySelector('input[name="channelName"]').value;
                const message = document.querySelector('input[name="message"]').value;

                socket.emit('submit public message', {'channelName': channelName, 'message': message});

                // reset form and prevent the default submit behavior
                document.querySelector('#messageForm').reset();
                return false;

            }

        });

        // listen for a broadcast of a public message
        socket.on('broadcast public message', data => {

            const currentChannel = document.querySelector('input[name="channelName"]').value;

            // only update the DOM if the broadcasted message is meant for the current channel
            if (currentChannel == data.channelName) {

                const context = {'message': data.publicMessage.message, 'timestamp': data.publicMessage.timestamp, 'username': data.publicMessage.username}
                const newMessage =  messageTemplate(context);
                document.querySelector('#channelMessages').innerHTML += newMessage;
                scrollPoint.scrollIntoView();

            }

        });

    }

    // add scripts for private channel template
    if (document.querySelector('#privateChannel')) {

        // page globals
        const scrollPoint = document.querySelector('#scrollPoint');

        // configure websocket event listeners
        socket.on('connect', () => {

            document.querySelector('#messageForm').onsubmit = () => {

                // get form data
                const otherUser = document.querySelector('input[name="otherUser"]').value;
                const message = document.querySelector('input[name="message"]').value;

                socket.emit('submit private message', {'otherUser': otherUser, 'message': message});

                // reset form and prevent the default submit behavior
                document.querySelector('#messageForm').reset();
                return false;

            }

        });

        // listen for a broadcast of a private message
        socket.on('broadcast private message', data => {

            const channelHash = document.querySelector('input[name="channelHash"]').value;

            // only update the DOM if the broadcasted message is meant for the current channel
            if (channelHash == data.channelHash) {

                const context = {'message': data.privateMessage.message, 'timestamp': data.privateMessage.timestamp, 'username': data.privateMessage.username}
                const newMessage =  messageTemplate(context);
                document.querySelector('#channelMessages').innerHTML += newMessage;
                scrollPoint.scrollIntoView();

            }

        });

    }

});