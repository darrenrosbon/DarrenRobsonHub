const reduceMotion = () => matchMedia('(prefers-reduced-motion: reduce)').matches;

// ---------- Email: assembled at runtime so scrapers never see the address in the HTML ----------
const email = ['darrenrobson2001.dr', 'gmail.com'].join('@');
document.querySelectorAll('[data-email]').forEach((a) => { a.href = 'mailto:' + email; });
document.querySelectorAll('[data-email-text]').forEach((el) => { el.textContent = email; });

// ---------- Smooth in-page scrolling, switched on at the first interaction (see html.smooth in styles.css) ----------
const smooth = () => document.documentElement.classList.add('smooth');
addEventListener('pointerdown', smooth, { once: true });
addEventListener('keydown', smooth, { once: true });

// ---------- Frosted nav gains a hairline once the page scrolls ----------
const nav = document.querySelector('.nav');
const onScroll = () => nav.classList.toggle('is-scrolled', window.scrollY > 4);
addEventListener('scroll', onScroll, { passive: true });
onScroll();

// ---------- Scroll spy: underline the menu link for the section in view ----------
const spyLinks = new Map([...document.querySelectorAll('.nav__text a')].map((a) => [a.hash.slice(1), a]));
const spy = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    const link = spyLinks.get(e.target.id);
    if (!link) return;
    if (e.isIntersecting) {
      spyLinks.forEach((l) => l.removeAttribute('aria-current'));
      link.setAttribute('aria-current', 'true');
    }
  });
}, { rootMargin: '-45% 0px -50% 0px' });
spyLinks.forEach((_, id) => { const el = document.getElementById(id); if (el) spy.observe(el); });
new IntersectionObserver(([e]) => { if (e.isIntersecting) spyLinks.forEach((l) => l.removeAttribute('aria-current')); })
  .observe(document.querySelector('.hero'));

// Appearance switch, toast and back to top live in common.js, shared with the other pages.
const root = document.documentElement;

// ---------- Mobile menu: native <dialog> gives focus trapping and Esc to close ----------
const menu = document.getElementById('menu');
const openBtn = document.getElementById('menu-open');
const closeMenu = () => menu.close();
openBtn.addEventListener('click', () => { menu.showModal(); root.classList.add('menu-open'); });
document.getElementById('menu-close').addEventListener('click', closeMenu);
menu.addEventListener('close', () => { root.classList.remove('menu-open'); openBtn.focus({ preventScroll: true }); });
menu.querySelectorAll('a').forEach((a) => a.addEventListener('click', closeMenu));
addEventListener('resize', () => { if (menu.open && innerWidth > 960) closeMenu(); });

// ---------- Work filters: show only the projects of one kind; without JS the buttons stay hidden and every project shows ----------
const filters = document.querySelector('.work__filters');
if (filters) {
  filters.hidden = false;
  const items = [...document.querySelectorAll('.work__item')];
  const announce = document.getElementById('status');
  filters.addEventListener('click', (e) => {
    const btn = e.target.closest('button[data-filter]');
    if (!btn) return;
    filters.querySelectorAll('button').forEach((b) => b.setAttribute('aria-pressed', String(b === btn)));
    const kind = btn.dataset.filter;
    items.forEach((li) => { li.hidden = kind !== 'all' && !li.dataset.kinds.split(' ').includes(kind); });
    if (announce) announce.textContent = `Showing ${items.filter((li) => !li.hidden).length} projects`;
  });
}

// ---------- Copy email: silent success, tick for 2 s, announced to screen readers ----------
document.querySelectorAll('[data-copy-email]').forEach((btn) => {
  const icon = btn.querySelector('use');
  const label = btn.getAttribute('aria-label');
  let timer;
  btn.addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(email); }
    catch { location.href = 'mailto:' + email; return; }
    icon.setAttribute('href', '#i-check');
    btn.dataset.state = 'done';
    btn.setAttribute('aria-label', 'Email address copied');
    toast('Email address copied');
    clearTimeout(timer);
    timer = setTimeout(() => {
      icon.setAttribute('href', '#i-copy');
      delete btn.dataset.state;
      btn.setAttribute('aria-label', label);
    }, 2000);
  });
});

// ---------- Hero photo flies into the nav: CSS scroll timeline does the motion, this only measures the path ----------
const photo = document.querySelector('.hero__photo');
const mark = document.querySelector('.nav .nav__mark');
if (photo && mark && CSS.supports('animation-timeline: scroll()')) {
  const measure = () => {
    root.classList.remove('fly'); // read the photo's resting position, not a mid-flight one
    const p = photo.getBoundingClientRect();
    const m = mark.getBoundingClientRect();
    const photoY = p.top + scrollY + p.height / 2;
    const navY = m.top + m.height / 2;
    // The flight ends exactly when normal scrolling would carry the photo up to the nav's height,
    // so it only needs to slide sideways and shrink on the way.
    root.style.setProperty('--fly-end', `${Math.max(1, photoY - navY)}px`);
    root.style.setProperty('--fly-x', `${m.left + 15 - (p.left + p.width / 2)}px`);
    root.style.setProperty('--fly-y', '0px');
    root.style.setProperty('--fly-s', String(30 / p.width));
    root.classList.add('fly');
  };
  let frame;
  addEventListener('resize', () => { cancelAnimationFrame(frame); frame = requestAnimationFrame(measure); });
  if (photo.complete) measure(); else photo.addEventListener('load', measure, { once: true });
}

// ---------- Background grid: faint blueprint lines with pulses that flare at crossings and run along the lines ----------
// After the background on darrenrosbon.github.io/darren-portfolio-site, redrawn with thin lines in the accent colour instead of ASCII.
// It is fixed to the viewport and slides with the page by whole grid cells, so it backs every section.
// Two stacked canvases keep it cheap: the lines are drawn once (again only on resize or theme change), and the
// animated layer on top only clears and redraws the small squares around each live pulse, about 30 times a second.
const grid = document.querySelector('.grid-bg');
if (grid) {
  const fx = grid.cloneNode();
  grid.after(fx);
  const ctx = grid.getContext('2d');
  const fctx = fx.getContext('2d');
  const GAP = 48;          // grid spacing in CSS pixels
  const LIFE = 1600;       // how long one pulse lasts, ms
  const REACH = GAP * 1.6; // how far a pulse's arms travel
  const FRAME = 1000 / 30; // pulses fade slowly, so 30 fps looks the same as 60 at half the work
  let W = 0, H = 0, ox = 0, dpr = 1, px = 1, nodes = [], pulses = [], dirty = [];
  let lastSpawn = 0, lastDraw = 0, frame = 0, visible = true;
  // Snap to whole device pixels so every line renders equally crisp, including at 125% or 150% display scaling,
  // where half-pixel positions would smear a faint line across two pixels and make some lines all but vanish.
  const snap = (v) => (Math.round(v * dpr) + (Math.round(px * dpr) % 2 ? 0.5 : 0)) / dpr; // odd widths sit on half pixels
  const pix = (v) => Math.round(v * dpr) / dpr;
  let rgb = '226, 128, 60', lineA = 0.1, pulseA = 0.45;

  const readColours = () => {
    const cs = getComputedStyle(root);
    rgb = cs.getPropertyValue('--grid-rgb').trim() || rgb;
    lineA = parseFloat(cs.getPropertyValue('--grid-line')) || lineA;
    pulseA = parseFloat(cs.getPropertyValue('--grid-pulse')) || pulseA;
  };
  const size = () => {
    dpr = Math.min(devicePixelRatio || 1, 2); // above 2x the extra sharpness isn't worth the memory
    // One extra cell of height lets the canvas slide up by up to a cell without showing a gap at the bottom.
    // Round to whole device pixels so the bitmap maps 1:1 onto the screen.
    const cssH = Math.round((innerHeight + GAP) * dpr) / dpr;
    px = Math.max(1, Math.floor(dpr)) / dpr; // line width: one CSS pixel, rounded to whole device pixels
    for (const [c, cx] of [[grid, ctx], [fx, fctx]]) {
      c.style.height = `${cssH}px`;
      const box = c.getBoundingClientRect();
      W = box.width; H = box.height;
      c.width = Math.round(W * dpr); c.height = Math.round(H * dpr);
      cx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    ox = (W / 2) % GAP; // centre the grid so it sits symmetrically behind the hero
    nodes = [];
    for (let x = ox; x <= W; x += GAP) for (let y = GAP / 2; y <= H; y += GAP) nodes.push([x, y]);
    dirty = [];
  };
  const drawGrid = () => {
    ctx.clearRect(0, 0, W, H);
    ctx.lineWidth = px;
    ctx.strokeStyle = `rgba(${rgb}, ${lineA})`;
    ctx.beginPath();
    for (let x = ox; x <= W; x += GAP) { ctx.moveTo(snap(x), 0); ctx.lineTo(snap(x), H); }
    for (let y = GAP / 2; y <= H; y += GAP) { ctx.moveTo(0, snap(y)); ctx.lineTo(W, snap(y)); }
    ctx.stroke();
    // small crosshairs mark each crossing, a touch stronger than the lines
    ctx.fillStyle = `rgba(${rgb}, ${Math.min(1, lineA * 2)})`;
    for (const [x, y] of nodes) { ctx.fillRect(pix(x) - 2, pix(y), 4 + px, px); ctx.fillRect(pix(x), pix(y) - 2, px, 4 + px); }
  };
  const drawPulses = (t) => {
    // wipe only what the last frame drew
    for (const [x, y, w, h] of dirty) fctx.clearRect(x, y, w, h);
    dirty = [];
    if (t - lastSpawn > 380 && nodes.length) {
      const n = 1 + Math.floor(Math.random() * 3);
      for (let i = 0; i < n; i++) pulses.push({ at: nodes[Math.floor(Math.random() * nodes.length)], start: t });
      lastSpawn = t;
    }
    pulses = pulses.filter((p) => t - p.start < LIFE);
    fctx.lineWidth = px;
    for (const { at: [x, y], start } of pulses) {
      const age = (t - start) / LIFE;
      const core = Math.max(0, 1 - age * 2.2) * pulseA;
      if (core > 0) { fctx.fillStyle = `rgba(${rgb}, ${core})`; fctx.fillRect(pix(x) - 2, pix(y) - 2, 4 + px, 4 + px); }
      // arms run out along the four lines and fade as they go
      const reach = age * REACH;
      const arm = (1 - age) * pulseA * 0.7;
      const g = (dx, dy) => {
        const grad = fctx.createLinearGradient(x, y, x + dx * reach, y + dy * reach);
        grad.addColorStop(0, `rgba(${rgb}, 0)`); grad.addColorStop(1, `rgba(${rgb}, ${arm})`);
        fctx.strokeStyle = grad;
        fctx.beginPath(); fctx.moveTo(snap(x), snap(y)); fctx.lineTo(dx ? snap(x + dx * reach) : snap(x), dy ? snap(y + dy * reach) : snap(y)); fctx.stroke();
      };
      if (reach > 1 && arm > 0.01) { g(1, 0); g(-1, 0); g(0, 1); g(0, -1); }
      const r = Math.max(reach, 3) + 3;
      dirty.push([x - r, y - r, r * 2, r * 2]);
    }
  };
  const loop = (t) => {
    if (t - lastDraw >= FRAME - 2) { drawPulses(t); lastDraw = t; }
    frame = requestAnimationFrame(loop);
  };
  const start = () => {
    cancelAnimationFrame(frame);
    if (reduceMotion() || !visible || document.hidden) return; // the still grid stays; pulses pause
    frame = requestAnimationFrame(loop);
  };
  const redraw = () => { readColours(); drawGrid(); };
  // Slide both layers with the page by whole device pixels, wrapping every cell, so the lines never blur and the loop is seamless.
  let slideFrame = 0;
  const slide = () => {
    slideFrame = 0;
    const cell = GAP * dpr;
    const y = -(Math.round(scrollY * dpr) % cell) / dpr;
    grid.style.transform = fx.style.transform = `translate3d(0, ${y}px, 0)`;
  };
  addEventListener('scroll', () => { if (!slideFrame) slideFrame = requestAnimationFrame(slide); }, { passive: true });

  readColours(); size(); drawGrid(); slide(); start();
  let resizeFrame;
  // Phone browsers resize the viewport as the address bar slides away; only rebuild when the width changes or the height outgrows the canvas.
  addEventListener('resize', () => {
    if (Math.abs(innerWidth - W) < 1 && innerHeight + GAP <= H + 1) return;
    cancelAnimationFrame(resizeFrame);
    resizeFrame = requestAnimationFrame(() => { size(); drawGrid(); slide(); });
  });
  new MutationObserver(redraw).observe(root, { attributes: true, attributeFilter: ['data-theme'] });
  document.addEventListener('visibilitychange', start);
}

// ---------- Numbers count up the first time they scroll into view ----------
const counters = document.querySelectorAll('[data-count]');
if (!reduceMotion() && 'IntersectionObserver' in window) {
  const run = (el) => {
    const end = Number(el.dataset.count);
    const start = performance.now();
    const tick = (now) => {
      const t = Math.min(1, (now - start) / 1100);
      el.textContent = Math.round(end * (1 - Math.pow(2, -10 * t))); // ease-out expo
      if (t < 1) requestAnimationFrame(tick); else el.textContent = end;
    };
    requestAnimationFrame(tick);
  };
  const seen = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) { seen.unobserve(e.target); run(e.target); } });
  }, { threshold: 0.6 });
  counters.forEach((el) => {
    el.dataset.count = el.textContent;
    // Screen readers get the final value straight away; the ticking digits are visual only.
    const sr = document.createElement('span');
    sr.className = 'sr';
    sr.textContent = el.textContent;
    el.before(sr);
    el.setAttribute('aria-hidden', 'true');
    el.textContent = '0';
    seen.observe(el);
  });
}

// ---------- Ripples: faint ASCII waves that spread from the cursor, over the whole page ----------
// Drawn only while a ripple is alive, so the page costs nothing when the cursor is still. Skipped for reduced motion.
const ascii = document.querySelector('.ascii-bg');
if (ascii && !reduceMotion()) {
  const ctx = ascii.getContext('2d');
  const RAMP = ' .·:;-=+*#%@';
  const CW = 8.4, CH = 15, LIFE = 2400, STEP = 45;
  let W = 0, H = 0, dpr = 1, rgb = '226, 128, 60', ripples = [], last = { x: -999, y: -999 }, frame = 0;

  const size = () => {
    dpr = Math.min(devicePixelRatio || 1, 2);
    W = document.documentElement.clientWidth; H = innerHeight;
    ascii.style.height = `${H}px`;
    ascii.width = Math.round(W * dpr); ascii.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  };
  const colours = () => { rgb = getComputedStyle(root).getPropertyValue('--grid-rgb').trim() || rgb; };
  const draw = (t) => {
    ripples = ripples.filter((r) => t - r.t < LIFE);
    ctx.clearRect(0, 0, W, H);
    if (!ripples.length) { frame = 0; return; }
    ctx.font = '14px ui-monospace, Consolas, "Courier New", monospace';
    for (const r of ripples) {
      // only the ring's neighbourhood can be marked, so walk just that box
      const age = (t - r.t) / 1000, front = age * 260, reach = front + 70;
      const x0 = Math.max(0, Math.floor((r.x - reach) / CW)), x1 = Math.min(Math.ceil(W / CW), Math.ceil((r.x + reach) / CW));
      const y0 = Math.max(0, Math.floor((r.y - reach) / CH)), y1 = Math.min(Math.ceil(H / CH), Math.ceil((r.y + reach) / CH));
      for (let j = y0; j < y1; j++) for (let i = x0; i < x1; i++) {
        const px = i * CW, py = j * CH;
        const dd = Math.hypot(px - r.x, (py - r.y) * 1.2) - front;
        const env = Math.exp(-dd * dd / 5000) * Math.exp(-age * 1.6) * r.a;
        if (env < 0.04) continue;
        const h = Math.min(1, Math.max(0, 0.5 + Math.cos(dd * 0.09) * env * 0.32));
        const k = Math.abs(h - 0.5) * 2;
        if (k < 0.06) continue;
        ctx.fillStyle = `rgba(${rgb}, ${0.05 + Math.min(1, k * 1.2 + env * 0.3) * 0.3})`;
        ctx.fillText(RAMP[Math.min(RAMP.length - 1, (h * RAMP.length) | 0)], px, py + CH - 3);
      }
    }
    frame = requestAnimationFrame(draw);
  };
  const spawn = (x, y, a) => {
    ripples.push({ x, y, t: performance.now(), a });
    if (!frame) frame = requestAnimationFrame(draw);
  };

  addEventListener('pointermove', (e) => {
    const x = e.clientX, y = e.clientY;
    if (Math.hypot(x - last.x, y - last.y) < STEP) return;
    last = { x, y };
    spawn(x, y, 0.7);
  }, { passive: true });
  addEventListener('pointerdown', (e) => {
    spawn(e.clientX, e.clientY, 1.2);
  }, { passive: true });

  size(); colours();
  addEventListener('resize', () => { if (Math.abs(innerWidth - W) >= 1 || innerHeight > H + 1) size(); });
  new MutationObserver(colours).observe(root, { attributes: true, attributeFilter: ['data-theme'] });
}

// ---------- Print: closed jobs wouldn't print, so open them all first ----------
addEventListener('beforeprint', () => document.querySelectorAll('.job').forEach((d) => { d.open = true; }));
