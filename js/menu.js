// Mobile menu toggle script
// Toggles visibility of nav links on small screens

function toggleMenu() {
  const nav = document.querySelector('nav ul');
  if (nav) {
    nav.classList.toggle('show');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const toggleButton = document.querySelector('.menu-toggle');
  if (toggleButton) {
    toggleButton.addEventListener('click', toggleMenu);
  }
});
