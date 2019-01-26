document.addEventListener('DOMContentLoaded', () => {

    // connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // add scripts for channel template
    if (document.querySelector('#publicChannel')) {

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

                const li = document.createElement('li');
                li.innerHTML = `${data.publicMessage.message} - ${data.publicMessage.timestamp} - ${data.publicMessage.username}`;
                document.querySelector('#channelMessages').append(li);

            }

        });

    }

});