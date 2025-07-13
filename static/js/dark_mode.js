const darkModeToggle = document.getElementById('dark-mode-toggle');
const root = document.documentElement;  // <html>

darkModeToggle.addEventListener('click', () => {
  root.classList.toggle('dark-mode');
});
