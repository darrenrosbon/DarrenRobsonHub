// Shared by every page: appearance switch, toast messages and back to top.
// Wrapped in a block so its names never clash with the home page's script.js.
{
  const root = document.documentElement;
  const status = document.getElementById('status');
  const still = () => matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---------- Toast: a short visual confirmation; screen readers hear it through the status region ----------
  let toastEl;
  let toastTimer;
  window.toast = (message) => {
    if (!toastEl) {
      toastEl = document.createElement('div');
      toastEl.className = 'toast';
      toastEl.setAttribute('aria-hidden', 'true');
      document.body.append(toastEl);
    }
    toastEl.innerHTML = '<svg viewBox="0 0 24 24"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg><span></span>';
    toastEl.querySelector('span').textContent = message;
    toastEl.classList.add('is-shown');
    if (status) status.textContent = message;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      toastEl.classList.remove('is-shown');
      if (status) status.textContent = '';
    }, 2400);
  };

  // ---------- Appearance: Light (the default) or Dark, remembered once chosen ----------
  const toggle = document.getElementById('theme-toggle');
  if (toggle) {
    const meta = document.querySelector('meta[name="theme-color"]');
    const NAMES = { light: 'Light', dark: 'Dark' };
    const ICONS = { light: '#i-sun', dark: '#i-moon' };
    let mode = root.dataset.theme === 'dark' ? 'dark' : 'light';

    const applyMode = () => {
      if (mode === 'dark') root.dataset.theme = 'dark'; else delete root.dataset.theme;
      if (meta) meta.content = mode === 'dark' ? '#141518' : '#ffffff'; // keep the browser's own bar in step
      const next = mode === 'dark' ? 'light' : 'dark';
      toggle.querySelector('use').setAttribute('href', ICONS[mode]);
      toggle.setAttribute('aria-label', `Appearance: ${NAMES[mode]}. Switch to ${NAMES[next]}`);
      toggle.title = `Appearance: ${NAMES[mode]}`;
    };
    toggle.addEventListener('click', () => {
      mode = mode === 'dark' ? 'light' : 'dark';
      try { mode === 'dark' ? localStorage.setItem('theme', 'dark') : localStorage.removeItem('theme'); } catch {}
      if (document.startViewTransition && !still()) document.startViewTransition(applyMode);
      else applyMode();
      if (status) status.textContent = `Appearance set to ${NAMES[mode]}`;
    });
    applyMode();
  }

  // ---------- Back to top: appears once the page has scrolled a fair way ----------
  const toTop = document.querySelector('.to-top');
  if (toTop) {
    const update = () => {
      const room = root.scrollHeight - innerHeight;
      // Long pages show it after a screen of scrolling; shorter ones once past halfway. Pages that barely scroll never do.
      toTop.classList.toggle('is-shown', room > innerHeight * 0.5 && scrollY > Math.min(innerHeight, room * 0.5));
    };
    addEventListener('scroll', update, { passive: true });
    update();
    toTop.addEventListener('click', () => {
      scrollTo({ top: 0, behavior: still() ? 'auto' : 'smooth' });
      // Keyboard users continue from the top of the page, not from the hidden button.
      document.querySelector('.nav__mark')?.focus({ preventScroll: true });
    });
  }
}
