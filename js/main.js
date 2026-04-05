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

  // --- 1. Scroll Reveal Animation (Intersection Observer) ---
  const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.15
  };

  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target); // Animate only once
      }
    });
  }, observerOptions);

  // Seleccionar tanto el hero como los stills y galerías de fotografía (si existen en la página)
  const animatableImages = document.querySelectorAll('.project-stills img, .project-hero-img, .collection-gallery img');
  animatableImages.forEach(img => {
    if (!img.classList.contains('scroll-reveal')) {
      img.classList.add('scroll-reveal'); // Agregar clase base
    }
    observer.observe(img);
  });

  // --- 2. Lightbox Functionality ---
  const stills = document.querySelectorAll('.project-stills img, .collection-gallery img');
  
  if (stills.length > 0) {
    // Crear el overlay
    const lightboxOverlay = document.createElement('div');
    lightboxOverlay.classList.add('lightbox-overlay');

    const lightboxImg = document.createElement('img');
    lightboxImg.classList.add('lightbox-img');

    const lightboxClose = document.createElement('span');
    lightboxClose.classList.add('lightbox-close');
    lightboxClose.innerHTML = '&times;';

    lightboxOverlay.appendChild(lightboxImg);
    lightboxOverlay.appendChild(lightboxClose);
    document.body.appendChild(lightboxOverlay);

    // Abrir lightbox al clickear un still
    stills.forEach(img => {
      img.style.cursor = 'zoom-in';
      img.addEventListener('click', () => {
        lightboxImg.src = img.src;
        lightboxImg.alt = img.alt;
        lightboxOverlay.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevenir scroll al abrir
      });
    });

    // Función para cerrar el lightbox
    const closeLightbox = () => {
      lightboxOverlay.classList.remove('active');
      document.body.style.overflow = ''; // Restaurar scroll
      // Removemos el src después de la transición de CSS (0.3s)
      setTimeout(() => {
        if (!lightboxOverlay.classList.contains('active')) {
          lightboxImg.src = '';
        }
      }, 300);
    };

    // Listeners para cerrar
    lightboxClose.addEventListener('click', closeLightbox);

    lightboxOverlay.addEventListener('click', (e) => {
      if (e.target === lightboxOverlay) {
         closeLightbox();
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && lightboxOverlay.classList.contains('active')) {
        closeLightbox();
      }
    });
  }
});
