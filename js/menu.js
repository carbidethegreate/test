// Mobile menu toggle script
// Toggles visibility of nav links on small screens

function toggleMenu() {
  const menu = document.querySelector('.navbar-menu');
  if (menu) {
    menu.classList.toggle('active');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const toggleButton = document.querySelector('.menu-toggle');
  if (toggleButton) {
    toggleButton.addEventListener('click', toggleMenu);
  }
});
