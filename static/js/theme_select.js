// Handles theme selection only
console.log('theme_select.js loaded');

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOMContentLoaded fired');
    const themeInput = document.getElementById('theme-input');
    const themeSelectButton = document.getElementById('theme-select-button');

    if (!themeInput) console.log('theme-input not found');
    if (!themeSelectButton) console.log('theme-select-button not found');

    themeSelectButton.addEventListener('click', () => {
        console.log('Theme select button clicked');
        const theme = themeInput.value.trim();
        if (!theme) {
            themeInput.classList.add('input-error');
            themeInput.placeholder = 'Please enter a category!';
            return;
        }
        window.location.href = `/themed/${encodeURIComponent(theme)}`;
    });

    themeInput.addEventListener('input', () => {
        themeInput.classList.remove('input-error');
        themeInput.placeholder = 'Type a category (e.g. scientists, athletes, etc.)...';
    });
});
