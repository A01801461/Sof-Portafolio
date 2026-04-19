/* ================================================
   Sofía Abud — Main Script
   ================================================ */

document.addEventListener('DOMContentLoaded', () => {
  // --- 0. Dynamic Color Scheme ---
  const accentColors = ['#4A5A46', '#6F7555', '#6B5448', '#87A19E', '#335765', '#8D623E'];
  const randomColor1 = accentColors[Math.floor(Math.random() * accentColors.length)];
  let randomColor2 = accentColors[Math.floor(Math.random() * accentColors.length)];
  
  // Optional: Ensure they are different if possible
  if (randomColor1 === randomColor2) {
    randomColor2 = accentColors[(accentColors.indexOf(randomColor1) + 1) % accentColors.length];
  }

  document.documentElement.style.setProperty('--accent-color', randomColor1);
  document.documentElement.style.setProperty('--accent-color-secondary', randomColor2);

  const siteName = document.querySelector('.site-name');
  const toggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelectorAll('.nav-list a');

  // Contextual navigation on site name click
  if (siteName) {
    siteName.addEventListener('click', () => {
      const path = window.location.pathname;
      
      if (document.title.includes('404')) {
        window.location.href = '/index.html';
      } else if (path.includes('/projects/')) {
        window.location.href = '../index.html';
      } else if (path.includes('/music/')) {
        window.location.href = '../music.html';
      } else if (path.includes('/photography/')) {
        window.location.href = '../photography.html';
      } else {
        window.location.reload();
      }
    });
  }

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
  const animatableImages = document.querySelectorAll('.project-stills img, .project-hero-img, .collection-gallery img, .about-image img');
  animatableImages.forEach(img => {
    if (!img.classList.contains('scroll-reveal')) {
      img.classList.add('scroll-reveal'); // Agregar clase base
    }
    observer.observe(img);
  });

  // --- 2. Lightbox Functionality ---
  const stills = document.querySelectorAll('.project-stills img, .collection-gallery img, .about-image img');
  let currentIndex = 0;

  if (stills.length > 0) {
    // Crear el overlay
    const lightboxOverlay = document.createElement('div');
    lightboxOverlay.classList.add('lightbox-overlay');

    const lightboxImg = document.createElement('img');
    lightboxImg.classList.add('lightbox-img');

    const lightboxClose = document.createElement('span');
    lightboxClose.classList.add('lightbox-close');
    lightboxClose.innerHTML = '&times;';

    // Contenedor para imagen y controles (para posicionamiento relativo)
    const lightboxContent = document.createElement('div');
    lightboxContent.classList.add('lightbox-content');

    // Botones de navegación
    const prevBtn = document.createElement('button');
    prevBtn.classList.add('lightbox-prev');
    prevBtn.innerHTML = '&#10094;'; // Flecha izquierda minimalista
    prevBtn.ariaLabel = 'Previous image';

    const nextBtn = document.createElement('button');
    nextBtn.classList.add('lightbox-next');
    nextBtn.innerHTML = '&#10095;'; // Flecha derecha minimalista
    nextBtn.ariaLabel = 'Next image';

    lightboxContent.appendChild(lightboxImg);
    lightboxContent.appendChild(prevBtn);
    lightboxContent.appendChild(nextBtn);

    lightboxOverlay.appendChild(lightboxContent);
    lightboxOverlay.appendChild(lightboxClose);
    document.body.appendChild(lightboxOverlay);

    // Función para mostrar imagen por índice
    const showImage = (index) => {
      if (index < 0) index = stills.length - 1;
      if (index >= stills.length) index = 0;
      currentIndex = index;

      const targetImg = stills[currentIndex];
      lightboxImg.src = targetImg.dataset.highRes || targetImg.src;
      lightboxImg.alt = targetImg.alt;
    };

    // Abrir lightbox al clickear un still
    stills.forEach((img, index) => {
      img.style.cursor = 'zoom-in';
      img.addEventListener('click', () => {
        showImage(index);
        lightboxOverlay.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevenir scroll al abrir
      });
    });

    // Eventos para botones
    prevBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      showImage(currentIndex - 1);
    });

    nextBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      showImage(currentIndex + 1);
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

    // Soporte para Swipe (móvil)
    let touchStartX = 0;
    let touchEndX = 0;

    lightboxOverlay.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    lightboxOverlay.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      handleSwipe();
    }, { passive: true });

    const handleSwipe = () => {
      const swipeThreshold = 50; // Mínimo de píxeles para considerar swipe
      if (touchEndX < touchStartX - swipeThreshold) {
        // Swipe left -> Next
        showImage(currentIndex + 1);
      }
      if (touchEndX > touchStartX + swipeThreshold) {
        // Swipe right -> Prev
        showImage(currentIndex - 1);
      }
    };

    document.addEventListener('keydown', (e) => {
      if (!lightboxOverlay.classList.contains('active')) return;

      if (e.key === 'Escape') {
        closeLightbox();
      } else if (e.key === 'ArrowLeft') {
        showImage(currentIndex - 1);
      } else if (e.key === 'ArrowRight') {
        showImage(currentIndex + 1);
      }
    });
  }

  // --- 3. Clipboard copy for mailto link fallback ---
  const emailBtn = document.getElementById('email-btn');
  if (emailBtn) {
    emailBtn.addEventListener('click', (e) => {
      const emailTextSpan = document.getElementById('email-text');
      if (emailTextSpan && navigator.clipboard) {
        const originalText = emailTextSpan.innerText;
        navigator.clipboard.writeText('sofiaabud@gmail.com').then(() => {
          emailTextSpan.innerText = "Copied to clipboard!";
          setTimeout(() => {
            emailTextSpan.innerText = originalText;
          }, 2000);
        }).catch(err => {
          console.error("No se pudo copiar al portapapeles:", err);
        });
      }
    });
  }

  // --- 4. Content Protection (Friction Layers) ---
  /**
   * Disables right-click and drag-and-drop strictly for <img> and <audio> elements.
   * This adds a layer of friction without breaking accessibility on the rest of the site.
   */
  const protectedTags = ['IMG', 'AUDIO'];

  // Prevent right-click context menu
  document.addEventListener('contextmenu', (e) => {
    if (protectedTags.includes(e.target.tagName)) {
      e.preventDefault();
    }
  }, false);

  // Prevent drag and drop (saves images by dragging to desktop)
  document.addEventListener('dragstart', (e) => {
    if (protectedTags.includes(e.target.tagName)) {
      e.preventDefault();
    }
  }, false);
});

