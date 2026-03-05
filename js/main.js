/* ================================================
   Sofía Abud — Main Script
   ================================================ */

document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelectorAll('.nav-list a');

  // Toggle mobile menu
  toggle.addEventListener('click', () => {
    document.body.classList.toggle('nav-open');
  });

  // Close menu on link click (mobile)
  navLinks.forEach(link => {
    link.addEventListener('click', () => {
      document.body.classList.remove('nav-open');
    });
  });
});
