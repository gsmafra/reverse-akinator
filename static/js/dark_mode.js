const darkModeToggle = document.getElementById('dark-mode-toggle');
const root = document.documentElement;  // <html>
const currentHour = new Date().getHours();

if (currentHour >= 19 || currentHour < 6) {
  root.classList.add('dark-mode');
}

darkModeToggle.addEventListener('click', () => {
  root.classList.toggle('dark-mode');
});
