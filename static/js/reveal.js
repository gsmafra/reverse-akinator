document.getElementById('reveal-button').addEventListener('click', function() {
    fetch('/reveal')
        .then(response => response.json())
        .then(data => {
            document.getElementById('revealed-character').textContent = `The character is: ${data.character}`;
        })
        .catch(error => console.error('Error:', error));
});
