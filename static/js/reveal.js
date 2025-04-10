document.getElementById('reveal-button').addEventListener('click', function() {
    fetch('/reveal')
        .then(response => response.json())
        .then(data => {
            document.body.classList.add('character-revealed');
            document.getElementById('revealed-character').textContent = `${data.character}`;

            // Create an image element
            const characterImage = document.createElement('img');
            characterImage.src = data.image_url;
            characterImage.alt = data.character; // Add alt text for accessibility
            characterImage.classList.add('revealed-image'); // Optional: Add a class for styling

            // Get the container where you want to display the image
            const imageContainer = document.getElementById('image-container'); // Make sure you have an element with this ID in your HTML

            // Clear any previous image (optional)
            imageContainer.innerHTML = '';

            // Append the image to the container
            imageContainer.appendChild(characterImage);
        })
        .catch(error => console.error('Error:', error));
});

document.getElementById('reset-button').addEventListener('click', function() {
    window.location.reload();
});
