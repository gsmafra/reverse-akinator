import { getDeviceId } from './device_id.js';

document.addEventListener('DOMContentLoaded', function() {
    fetch('/reset', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ device_id: getDeviceId() })
    })
    .then(response => {
        if (!response.ok) {
            console.error('Error resetting character on load:', response.status);
        }
        return response.json();
    })
    .then(data => {
        console.log('Reset successful on load:', data.message);
    })
    .catch(error => {
        console.error('Error calling /reset on load:', error);
    });
});

document.getElementById('reset-button').addEventListener('click', function() {
    fetch('/reset', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ device_id: getDeviceId() })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        window.location.reload();
    })
    .catch(error => console.error('Error resetting on button click:', error));
});
