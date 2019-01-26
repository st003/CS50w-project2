document.addEventListener('DOMContentLoaded', () => {

    // connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // add scripts for channel template
    if (document.querySelector('#channel')) {

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

    }

});