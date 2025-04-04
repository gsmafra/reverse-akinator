const darkModeToggle = document.getElementById('dark-mode-toggle');
const body = document.body;
const sidebar = document.getElementById('session-history');
const currentHour = new Date().getHours();

if (currentHour >= 19 || currentHour < 6) {
  body.classList.add('dark-mode');
  sidebar.classList.toggle('dark-mode');
}

darkModeToggle.addEventListener('click', () => {
  body.classList.toggle('dark-mode');
  sidebar.classList.toggle('dark-mode');
});
