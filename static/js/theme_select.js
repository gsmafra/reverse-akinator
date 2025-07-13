import { getDeviceId } from './device_id.js';

// Handles theme selection and starts the themed game

console.log('theme_select.js loaded');

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOMContentLoaded fired');
    const themeInput = document.getElementById('theme-input');
    const themeSelectButton = document.getElementById('theme-select-button');
    const themeSelectContainer = document.getElementById('theme-select-container');
    const themedGameContainer = document.getElementById('themed-game-container');
    const themeTitle = document.getElementById('theme-title');

    if (!themeInput) console.log('theme-input not found');
    if (!themeSelectButton) console.log('theme-select-button not found');
    if (!themeSelectContainer) console.log('theme-select-container not found');
    if (!themedGameContainer) console.log('themed-game-container not found');
    if (!themeTitle) console.log('theme-title not found');

    themeSelectButton.addEventListener('click', () => {
        console.log('Theme select button clicked');
        const theme = themeInput.value.trim();
        const deviceId = getDeviceId();
        console.log('Theme:', theme, 'Device ID:', deviceId);
        if (!theme) {
            themeInput.classList.add('input-error');
            themeInput.placeholder = 'Please enter a category!';
            return;
        }
        if (!deviceId) {
            themeInput.classList.add('input-error');
            themeInput.placeholder = 'Device ID missing. Please refresh.';
            return;
        }

        // Call API to start themed game
        fetch('/start-themed-game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ category: theme, device_id: deviceId })
        })
        .then(async response => {
            let data;
            try {
                data = await response.json();
            } catch (e) {
                data = {};
            }
            console.log('Response:', response.status, data);
            if (!response.ok) {
                const errorMsg = data.error || 'Failed to start themed game';
                themeInput.classList.add('input-error');
                themeInput.placeholder = errorMsg;
                return;
            }
            // Proceed to game UI
            themeSelectContainer.style.display = 'none';
            themedGameContainer.style.display = '';
            themeTitle.textContent = `Theme: ${theme}`;
            window.selectedTheme = theme;
            const event = new CustomEvent('themeSelected', { detail: { theme } });
            document.dispatchEvent(event);
            console.log('Theme game started successfully');
        })
        .catch(error => {
            console.error('Fetch error:', error);
            themeInput.classList.add('input-error');
            themeInput.placeholder = 'Server error. Try again.';
        });
    });

    themeInput.addEventListener('input', () => {
        themeInput.classList.remove('input-error');
        themeInput.placeholder = 'Type a category (e.g. scientists, athletes, etc.)...';
    });

    const themedResetButton = document.getElementById('themed-reset-button');
    if (themedResetButton) {
        themedResetButton.addEventListener('click', () => {
            const theme = window.selectedTheme;
            const deviceId = getDeviceId();
            if (!theme || !deviceId) {
                alert('Theme or device ID missing.');
                return;
            }
            fetch('/start-themed-game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ category: theme, device_id: deviceId })
            })
            .then(async response => {
                let data;
                try {
                    data = await response.json();
                } catch (e) {
                    data = {};
                }
                if (!response.ok) {
                    alert(data.error || 'Failed to reset themed game.');
                    return;
                }
                // Optionally update UI with new character, or reload
                window.location.reload();
            })
            .catch(error => {
                console.error('Error resetting themed game:', error);
                alert('Server error. Try again.');
            });
        });
    }
});
