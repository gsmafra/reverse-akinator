document.addEventListener('DOMContentLoaded', function() {
    resetCharacter(); // Call the reset function when the page loads
});

function resetCharacter() {
    fetch('/reset', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            console.error('Error resetting character:', response.status);
            // Optionally display a message to the user
        }
        return response.json();
    })
    .then(data => {
        console.log('Reset successful:', data.message);
        // Optionally display a confirmation message to the user
    })
    .catch(error => {
        console.error('Error calling /reset:', error);
        // Optionally display an error message to the user
    });
}
