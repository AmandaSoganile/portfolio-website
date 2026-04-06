/* ============================================================
   CONFIG
   ============================================================ */
const API_BASE = '';

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
   HERO
   ============================================================ */
function initHero(about) {
  document.getElementById('hero-role').textContent = '\u2726 ' + about.tagline;
  document.getElementById('hero-firstname').textContent = about.name.split(' ')[0];
  document.getElementById('hero-lastname').textContent = about.name.split(' ').slice(-1)[0] + '.';
}

/* ============================================================
   MAIN
   ============================================================ */
async function init() {
  initTheme();
  initScrollReveal();

  const [about, facts, projects, books, songs] = await Promise.all([
    api('/about').catch(() => null),
    api('/fun-fact/all').catch(() => []),
    api('/projects').catch(() => []),
    api('/books').catch(() => ({ mine: [], community: [] })),
    api('/songs').catch(() => ({ mine: [], community: [] })),
  ]);

  if (about) { initHero(about); initAbout(about); }
  initFunFacts(facts);
  initProjects(projects);
  initBooks(books);
  initSongs(songs);

  initContact();
  initBooksForm();
  initSongsForm();
}

/* ============================================================
   STUBS — sections not yet implemented
   ============================================================ */
function initAbout(about) {
  document.getElementById('about-bio').textContent     = about.bio;
  document.getElementById('about-meaning').textContent = about.name_meaning;
  document.getElementById('about-goal').textContent    = '"' + about.life_goal + '"';

  // Extra personality blocks
  const left = document.querySelector('.about-left');
  if (about.quirky_talent) {
    const el = document.createElement('div');
    el.className = 'about-extra';
    el.innerHTML = `<strong>Quirky talent</strong>${about.quirky_talent}`;
    left.appendChild(el);
  }
  if (about.what_drives_me) {
    const el = document.createElement('div');
    el.className = 'about-extra';
    el.innerHTML = `<strong>What drives me</strong>${about.what_drives_me}`;
    left.appendChild(el);
  }

  // Chips
  const lovesEl    = document.getElementById('about-loves');
  const learningEl = document.getElementById('about-learning');

  (about.things_i_love || []).forEach(item => {
    const c = document.createElement('span');
    c.className = 'chip';
    c.textContent = item;
    lovesEl.appendChild(c);
  });

  (about.currently_learning || []).forEach(item => {
    const c = document.createElement('span');
    c.className = 'chip chip-current';
    c.textContent = item;
    learningEl.appendChild(c);
  });
}
function initProjects(projects) {
  const grid = document.getElementById('projects-grid');
  if (!projects || projects.length === 0) return;

  const p = projects[0];
  grid.className = 'proj-featured';
  grid.innerHTML = `
    <div class="proj-info">
      <div class="proj-tag">
        <span class="proj-tag-dot"></span>
        ${p.status === 'completed' ? 'Completed' : 'In progress'}
      </div>
      <div class="proj-name">${p.name}</div>
      <p class="proj-desc">${p.description}</p>
      <div class="proj-tech">
        ${(p.tech || []).map(t => `<span class="proj-tech-chip">${t}</span>`).join('')}
      </div>
      <div class="proj-links">
        ${p.links?.live ? `<a href="${p.links.live}" class="proj-link proj-link-primary" target="_blank">View live &rarr;</a>` : ''}
        ${p.links?.github ? `<a href="${p.links.github}" class="proj-link proj-link-ghost" target="_blank">GitHub</a>` : ''}
      </div>
    </div>
    <div class="proj-screens">
      <div class="proj-screen proj-screen-main">
        <span class="proj-screen-label">Dashboard</span>
      </div>
      <div class="proj-screen-row">
        <div class="proj-screen">
          <span class="proj-screen-label">Add Animal</span>
        </div>
        <div class="proj-screen">
          <span class="proj-screen-label">Health Records</span>
        </div>
      </div>
    </div>
  `;
}
function initBooks(data) {
  const BOOKS_PALETTE = [
    { base: '#8B1A1A', light: '#C0392B' }, // deep red
    { base: '#1A3A5C', light: '#2E6DA4' }, // navy
    { base: '#2D5A27', light: '#4A8C42' }, // forest green
    { base: '#6B3A2A', light: '#9C5B3A' }, // burnt sienna
    { base: '#4A3060', light: '#7B52A0' }, // plum
    { base: '#1A4A4A', light: '#2E8080' }, // dark teal
    { base: '#7A5200', light: '#B8860B' }, // antique gold
    { base: '#3A2A1A', light: '#7A5C3A' }, // dark leather
  ];
  const shelf = document.getElementById('books-shelf');
  (data.mine || []).forEach((book, i) => {
    const { base, light } = BOOKS_PALETTE[i % BOOKS_PALETTE.length];
    const el = document.createElement('div');
    el.className = 'book-spine';
    el.style.background = `linear-gradient(to right, ${base}, ${light} 40%, ${light} 70%, ${base})`;
    el.innerHTML = `
      <div class="book-spine-text">${book.title}</div>
      <div class="book-click-hint">click</div>
    `;
    el.addEventListener('click', () => openBookModal(book));
    shelf.appendChild(el);
  });

  const community = document.getElementById('books-community');
  (data.community || []).forEach(book => {
    const chip = document.createElement('div');
    chip.className = 'community-book-chip';
    chip.innerHTML = `${book.title} <span>— ${book.name}</span>`;
    community.appendChild(chip);
  });
}

async function openBookModal(book) {
  const modal = document.getElementById('book-modal');
  const cover = document.getElementById('book-modal-cover');
  const title = document.getElementById('book-modal-title');
  const author = document.getElementById('book-modal-author');

  title.textContent = book.title;
  author.textContent = book.author;
  cover.style.display = 'none';
  cover.src = '';
  modal.classList.add('open');

  try {
    const q = encodeURIComponent(book.title + ' ' + book.author);
    const res = await fetch(`https://openlibrary.org/search.json?q=${q}&limit=1`);
    const json = await res.json();
    const coverId = json.docs?.[0]?.cover_i;
    if (coverId) {
      const url = `https://covers.openlibrary.org/b/id/${coverId}-L.jpg`;
      cover.onload = () => { cover.style.display = 'block'; };
      cover.onerror = () => { cover.style.display = 'none'; };
      cover.src = url;
    }
  } catch (e) {
    console.error('cover fetch failed', e);
  }
}
function initSongs(data) {
  const ICONS = ['🎵', '🎶', '🎸', '🥁', '🎹', '🎤'];
  const list = document.getElementById('songs-mine');
  (data.mine || []).forEach((song, i) => {
    const row = document.createElement('div');
    row.className = 'song-row';
    row.innerHTML = `
      <span class="song-num">${String(i + 1).padStart(2, '0')}</span>
      <div class="song-icon">${ICONS[i % ICONS.length]}</div>
      <div class="song-info">
        <div class="song-title">${song.title}</div>
        <div class="song-artist">${song.artist}</div>
      </div>
    `;
    list.appendChild(row);
  });

  const community = document.getElementById('songs-community');
  (data.community || []).forEach(song => {
    const row = document.createElement('div');
    row.className = 'community-song-row';
    row.innerHTML = `
      <div class="community-song-title">${song.title} — <span style="font-weight:400">${song.artist || ''}</span></div>
      <div class="community-song-meta">added by ${song.name}${song.note ? ' · ' + song.note : ''}</div>
    `;
    community.appendChild(row);
  });
}
function initContact() {
  const form = document.getElementById('contact-form');
  if (!form) return;
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const btn = form.querySelector('button');
    btn.textContent = 'Sending...';
    btn.disabled = true;
    try {
      await api('/contact', { method: 'POST', body: JSON.stringify(Object.fromEntries(new FormData(form))) });
      btn.textContent = 'Sent ✓';
      form.reset();
    } catch (_) {
      btn.textContent = 'Failed — try again';
      btn.disabled = false;
    }
  });
}
function initBooksForm() {
  const form = document.getElementById('books-form');
  if (!form) return;
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form));
    await api('/books', { method: 'POST', body: JSON.stringify(data) });
    const chip = document.createElement('div');
    chip.className = 'community-book-chip';
    chip.innerHTML = `${data.title} <span>— ${data.name}</span>`;
    document.getElementById('books-community').appendChild(chip);
    form.reset();
  });
}
function initSongsForm() {
  const form = document.getElementById('songs-form');
  if (!form) return;
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form));
    await api('/songs', { method: 'POST', body: JSON.stringify(data) });
    const row = document.createElement('div');
    row.className = 'community-song-row';
    row.innerHTML = `
      <div class="community-song-title">${data.title} — <span style="font-weight:400">${data.artist || ''}</span></div>
      <div class="community-song-meta">added by ${data.name}${data.note ? ' · ' + data.note : ''}</div>
    `;
    document.getElementById('songs-community').appendChild(row);
    form.reset();
  });
}

/* ============================================================
   FUN FACTS
   ============================================================ */
function initFunFacts(facts) {
  const section = document.getElementById('fun-facts');
  const grid    = document.getElementById('facts-grid');

  const EMOJIS = ['😂', '💀', '😭', '🫶', '👀'];
  grid.innerHTML = facts.map((f, i) => `
    <div class="fact-card">
      <div class="fact-num">#${String(f.id).padStart(2, '0')}</div>
      <p class="fact-text">${f.fact}</p>
      <div class="fact-reactions">
        ${EMOJIS.map(emoji => `
          <button class="reaction-btn" onclick="addReaction(${f.id}, '${emoji}', this)">
            ${emoji} <span class="reaction-count">${f.reactions?.[emoji] || 0}</span>
          </button>
        `).join('')}
      </div>
    </div>
  `).join('');

  const cards = [...grid.querySelectorAll('.fact-card')];

  new IntersectionObserver(([e]) => {
    if (!e.isIntersecting) return;

    // Step 1: letters fly in from vertical positions → spread horizontally
    section.classList.add('ff-in');

    // Step 2: after spread, fade letters and reveal cards one by one
    setTimeout(() => {
      section.classList.add('cards-in');
      cards.forEach((card, i) => {
        setTimeout(() => card.classList.add('visible'), i * 150);
      });
    }, 1200);

  }, { threshold: 0.1 }).observe(section);
}

async function addReaction(factId, emoji, btn) {
  try {
    const data = await api(`/fun-fact/${factId}/react`, {
      method: 'POST',
      body: JSON.stringify({ emoji }),
    });
    btn.querySelector('.reaction-count').textContent = data.reactions[emoji] || 0;
    btn.classList.toggle('reacted');
  } catch (e) {
    showToast('Could not save reaction');
  }
}

document.addEventListener('DOMContentLoaded', init);
