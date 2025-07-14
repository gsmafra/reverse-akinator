import { getDeviceId } from './device_id.js';

console.log('themed_game.js loaded');

document.addEventListener('DOMContentLoaded', () => {
    // Get category from a data attribute or from the URL
    let category = null;
    if (window.categoryFromTemplate) {
        category = window.categoryFromTemplate;
    } else {
        // Try to extract from URL: /themed/{category}
        const match = window.location.pathname.match(/\/themed\/(.+)$/);
        if (match) category = decodeURIComponent(match[1]);
    }
    if (!category) {
        console.error('No category found for themed game.');
        return;
    }
    const deviceId = getDeviceId();
    // Optionally display the category in the UI
    const themeTitle = document.getElementById('theme-title');
    if (themeTitle) themeTitle.textContent = `Theme: ${category}`;

    // Start a new themed game on load
    fetch('/start-themed-game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ category, device_id: deviceId })
    })
    .then(async response => {
        let data;
        try { data = await response.json(); } catch (e) { data = {}; }
        if (!response.ok) {
            alert(data.error || 'Failed to start themed game.');
            return;
        }
        // Optionally update UI with new character, etc.
        // You can trigger a UI reset here if needed
    })
    .catch(error => {
        console.error('Error starting themed game:', error);
        alert('Server error. Try again.');
    });

    // No JS needed to show reset button; reveal.js will add 'character-revealed' class to <body>

    // Add reset button handler to reload with the correct category
    const themedResetButton = document.getElementById('themed-reset-button');
    if (themedResetButton) {
        themedResetButton.addEventListener('click', () => {
            window.location.href = `/themed/${encodeURIComponent(category)}`;
        });
    }

    // ...rest of your themed game logic...
});
