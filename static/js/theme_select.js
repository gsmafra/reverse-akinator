// Handles theme selection and starts the themed game

document.addEventListener('DOMContentLoaded', () => {
    const themeInput = document.getElementById('theme-input');
    const themeSelectButton = document.getElementById('theme-select-button');
    const themeSelectContainer = document.getElementById('theme-select-container');
    const themedGameContainer = document.getElementById('themed-game-container');
    const themeTitle = document.getElementById('theme-title');

    themeSelectButton.addEventListener('click', () => {
        const theme = themeInput.value.trim();
        if (!theme) {
            themeInput.classList.add('input-error');
            themeInput.placeholder = 'Please enter a category!';
            return;
        }
        // Hide theme selection, show game UI
        themeSelectContainer.style.display = 'none';
        themedGameContainer.style.display = '';
        themeTitle.textContent = `Theme: ${theme}`;
        // Optionally, store theme globally for use in submit.js or elsewhere
        window.selectedTheme = theme;
        // Optionally, trigger a custom event for other modules
        const event = new CustomEvent('themeSelected', { detail: { theme } });
        document.dispatchEvent(event);
    });

    themeInput.addEventListener('input', () => {
        themeInput.classList.remove('input-error');
        themeInput.placeholder = 'Type a category (e.g. scientists, athletes, etc.)...';
    });
});
