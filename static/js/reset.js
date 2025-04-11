import { getDeviceId } from './device_id.js';

document.addEventListener('DOMContentLoaded', function() {
    resetCharacter();
});

function resetCharacter() {
    fetch('/reset', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ device_id: getDeviceId() })
    })
    .then(response => {
        if (!response.ok) {
            console.error('Error resetting character:', response.status);
        }
        return response.json();
    })
    .then(data => {
        console.log('Reset successful:', data.message);
    })
    .catch(error => {
        console.error('Error calling /reset:', error);
    });
}
