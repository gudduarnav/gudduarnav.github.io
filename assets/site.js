(() => {
  const root = document.documentElement;
  const themeToggle = document.querySelector('.theme-toggle');
  const menuToggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#section-navigation');
  const links = [...nav.querySelectorAll('a')];
  const sections = links.map(link => document.querySelector(link.hash));
  const mobile = window.matchMedia('(max-width: 1080px)');
  const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
  let chosenTheme = false;
  try { chosenTheme = ['light', 'dark'].includes(localStorage.getItem('arnav-theme')); } catch { /* Optional storage. */ }

  function updateTheme(theme) {
    root.dataset.theme = theme;
    const dark = theme === 'dark';
    themeToggle.setAttribute('aria-pressed', String(dark));
    const text = dark ? themeToggle.dataset.dark : themeToggle.dataset.light;
    themeToggle.setAttribute('aria-label', `${themeToggle.dataset.label}: ${text}`);
    themeToggle.querySelector('.theme-text').textContent = text;
    themeToggle.querySelector('.theme-icon').textContent = dark ? '☾' : '☼';
    document.querySelector('meta[name="theme-color"]').content = dark ? '#11151e' : '#f6f7fb';
  }
  updateTheme(root.dataset.theme);
  themeToggle.addEventListener('click', () => {
    const theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    chosenTheme = true;
    updateTheme(theme);
    try { localStorage.setItem('arnav-theme', theme); } catch { /* The toggle still works. */ }
  });
  systemTheme.addEventListener('change', event => {
    if (!chosenTheme) updateTheme(event.matches ? 'dark' : 'light');
  });

  function setMenu(open, returnFocus = false) {
    root.classList.toggle('menu-open', open);
    menuToggle.setAttribute('aria-expanded', String(open));
    menuToggle.querySelector('.menu-text').textContent = open ? menuToggle.dataset.close : menuToggle.dataset.open;
    if (open) links[0].focus();
    if (returnFocus) menuToggle.focus();
  }
  menuToggle.addEventListener('click', () => setMenu(menuToggle.getAttribute('aria-expanded') !== 'true'));
  links.forEach(link => link.addEventListener('click', () => {
    if (mobile.matches) {
      setMenu(false);
      const section = document.querySelector(link.hash);
      section.setAttribute('tabindex', '-1');
      section.focus({ preventScroll: true });
    }
  }));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && root.classList.contains('menu-open')) setMenu(false, true);
  });
  document.addEventListener('click', event => {
    if (root.classList.contains('menu-open') && !nav.contains(event.target) && !menuToggle.contains(event.target)) setMenu(false);
  });
  document.addEventListener('focusin', event => {
    if (root.classList.contains('menu-open') && !nav.contains(event.target) && !menuToggle.contains(event.target)) setMenu(false);
  });
  mobile.addEventListener('change', () => setMenu(false));

  // The language link keeps the current chapter and works without JavaScript too.
  const languageLink = document.querySelector('.language-switch');
  const languagePath = languageLink.getAttribute('href');
  function syncLanguageLink() { languageLink.setAttribute('href', languagePath + window.location.hash); }
  window.addEventListener('hashchange', syncLanguageLink);
  syncLanguageLink();

  let scheduled = false;
  function updateActiveSection() {
    const marker = Math.min(window.innerHeight * 0.3, 240);
    let active = sections[0];
    for (const section of sections) {
      if (section.getBoundingClientRect().top <= marker) active = section;
    }
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 5) active = sections.at(-1);
    links.forEach(link => {
      const current = link.hash === `#${active.id}`;
      link.classList.toggle('active', current);
      if (current) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
    scheduled = false;
  }
  window.addEventListener('scroll', () => {
    if (!scheduled) { scheduled = true; requestAnimationFrame(updateActiveSection); }
  }, { passive: true });
  updateActiveSection();
})();
