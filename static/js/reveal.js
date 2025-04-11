import { getDeviceId } from './device_id.js';

document.getElementById('reveal-button').addEventListener('click', function() {
    fetch(`/reveal?device_id=${getDeviceId()}`)
        .then(response => response.json())
        .then(data => {
            document.body.classList.add('character-revealed');
            document.getElementById('revealed-character').textContent = `${data.character}`;
            const characterImage = document.createElement('img');
            characterImage.src = data.image_url;
            characterImage.alt = data.character;
            characterImage.classList.add('revealed-image');
            const imageContainer = document.getElementById('image-container');
            imageContainer.innerHTML = '';
            imageContainer.appendChild(characterImage);
        })
        .catch(error => console.error('Error:', error));
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
    .catch(error => console.error('Error resetting:', error));
});
