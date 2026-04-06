/* ============================================================
   CONFIG
   ============================================================ */
const API_BASE = 'http://127.0.0.1:5000';

async function api(path, opts = {}) {
  const defaults = { headers: { 'Content-Type': 'application/json' } };
  const res = await fetch(API_BASE + path, { ...defaults, ...opts });
  if (!res.ok) throw new Error(`API ${res.status}: ${path}`);
  return res.json();
}

/* ============================================================
   THEME
   ============================================================ */
function initTheme() {
  const saved = localStorage.getItem('portfolio-theme') || 'dark';
  document.documentElement.setAttribute('data-theme', saved);
  updateThemeBtn(saved);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('portfolio-theme', next);
  updateThemeBtn(next);
}

function updateThemeBtn(theme) {
  const btn = document.getElementById('theme-btn');
  if (btn) btn.textContent = theme === 'dark' ? '\u2600 Light' : '\u25D1 Dark';
}

/* ============================================================
   TOAST
   ============================================================ */
function showToast(msg, ms = 2800) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), ms);
}

/* ============================================================
   SCROLL REVEAL
   ============================================================ */
function initScrollReveal() {
  const els = document.querySelectorAll('.reveal, .reveal-l, .reveal-r');
  const obs = new IntersectionObserver(
    (entries) => entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); }),
    { threshold: 0.12 }
  );
  els.forEach(el => obs.observe(el));
}

/* ============================================================
   MAIN
   ============================================================ */
async function init() {
  initTheme();
  initScrollReveal();

  try {
    const [about, facts, projects, books, songs] = await Promise.all([
      api('/about'),
      api('/fun-fact/all'),
      api('/projects'),
      api('/books'),
      api('/songs'),
    ]);

    initHero(about);
    initAbout(about);
    initFunFacts(facts);
    initProjects(projects);
    initBooks(books);
    initSongs(songs);
  } catch (e) {
    console.error('API fetch failed:', e);
  }

  initContact();
  initBooksForm();
  initSongsForm();
}

document.addEventListener('DOMContentLoaded', init);
