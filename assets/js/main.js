// Mobile nav toggle
document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('.menu-toggle');
  const links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-controls', 'nav-links');
    if (!links.id) links.id = 'nav-links';

    const setOpen = (open) => {
      links.classList.toggle('open', open);
      document.body.classList.toggle('menu-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      toggle.textContent = open ? '✕' : '☰';
    };

    toggle.addEventListener('click', (e) => {
      e.stopPropagation();
      setOpen(!links.classList.contains('open'));
    });

    links.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => setOpen(false));
    });

    document.addEventListener('click', (e) => {
      if (!links.classList.contains('open')) return;
      if (!links.contains(e.target) && e.target !== toggle) setOpen(false);
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && links.classList.contains('open')) setOpen(false);
    });

    window.addEventListener('resize', () => {
      if (window.innerWidth > 880 && links.classList.contains('open')) setOpen(false);
    });
  }

  // Carousel
  document.querySelectorAll('.carousel').forEach(initCarousel);

  // Smooth nav highlight (active link by current page)
  const path = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(a => {
    const href = a.getAttribute('href');
    if (href === path) a.classList.add('active');
    if (path === '' && href === 'index.html') a.classList.add('active');
  });

  // Form fake handler
  document.querySelectorAll('form[data-handler="contact"]').forEach(f => {
    f.addEventListener('submit', e => {
      e.preventDefault();
      const msg = document.createElement('div');
      msg.className = 'alert';
      msg.textContent = 'Thanks! Your message has been received. For urgent towing call 0409 739 332.';
      f.replaceWith(msg);
    });
  });
});

function initCarousel(root) {
  const track = root.querySelector('.carousel-track');
  const slides = Array.from(root.querySelectorAll('.carousel-slide'));
  const prev = root.querySelector('.carousel-btn.prev');
  const next = root.querySelector('.carousel-btn.next');
  const dotsWrap = root.querySelector('.carousel-dots');
  if (!track || slides.length === 0) return;
  let i = 0;
  let timer;

  // Build dots
  if (dotsWrap) {
    slides.forEach((_, idx) => {
      const b = document.createElement('button');
      b.setAttribute('aria-label', `Slide ${idx + 1}`);
      b.addEventListener('click', () => go(idx, true));
      dotsWrap.appendChild(b);
    });
  }

  function go(n, manual) {
    i = (n + slides.length) % slides.length;
    track.style.transform = `translateX(-${i * 100}%)`;
    if (dotsWrap) Array.from(dotsWrap.children).forEach((d, idx) => d.classList.toggle('active', idx === i));
    if (manual) restart();
  }
  function restart() { clearInterval(timer); timer = setInterval(() => go(i + 1), 5000); }

  prev?.addEventListener('click', () => go(i - 1, true));
  next?.addEventListener('click', () => go(i + 1, true));
  go(0);
  restart();

  // Pause on hover
  root.addEventListener('mouseenter', () => clearInterval(timer));
  root.addEventListener('mouseleave', restart);
}
