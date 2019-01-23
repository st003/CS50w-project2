document.addEventListener('DOMContentLoaded', () => {

    // add scripts for channel template
    if (document.querySelector('#channel')) {

        // render messages on page load
        const channelName = document.querySelector('input[name="channelName"]').value;

        const getMessages = new XMLHttpRequest();
        getMessages.open('GET', `/messages/get/${channelName}`);
        getMessages.onload = () => {

            const response = JSON.parse(getMessages.responseText);

            if (!response.result) {

                alert(`${response.message}`);

            } else {

                let messageHTML = '';
                response.content.forEach( (message) => {

                    messageHTML += `<div>${message.username} - ${message.message} - ${message.timestamp}</div>`

                });

                document.querySelector('#messages').innerHTML = messageHTML;

            }

        }

        getMessages.send();

        // add form submit listener
        document.querySelector('#messageForm').onsubmit = () => {

            const request = new XMLHttpRequest();

            // get form data
            const channelName = document.querySelector('input[name="channelName"]').value;
            const message = document.querySelector('input[name="message"]').value;

            request.open('POST', '/messages/post');

            // define behavior once request has been made
            request.onload = () => {

                const response = JSON.parse(request.responseText);
                
                if (!response.result) {
                    alert(`${response.message}`);

                } else {
                    document.querySelector('#messageForm').reset();
                }                 

            }

            // construct the form data
            const postData = new FormData();
            postData.append('channelName', channelName);
            postData.append('message', message);

            // fire off the request and ignore the default form functionality
            request.send(postData);
            return false;

        }

    }

});