/* ============================================================
   CONFIG
   ============================================================ */
const API_BASE = '/api';

async function api(path, opts = {}) {
  const defaults = { headers: { 'Content-Type': 'application/json' } };
  const res = await fetch(API_BASE + path, { ...defaults, ...opts });
  if (!res.ok) throw new Error(`API ${res.status}: ${path}`);
  return res.json();
}

/* ============================================================
   THEME
   ============================================================ */
const THEMES = ['dark', 'light', 'pink'];
const THEME_LABELS = { dark: '☀ Light', light: '🌸 Pink', pink: '◑ Dark' };

function initTheme() {
  const saved = localStorage.getItem('portfolio-theme') || 'dark';
  document.documentElement.setAttribute('data-theme', saved);
  updateThemeBtn(saved);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  const idx = THEMES.indexOf(current);
  const next = THEMES[(idx + 1) % THEMES.length];
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('portfolio-theme', next);
  updateThemeBtn(next);
}

function updateThemeBtn(theme) {
  const btn = document.getElementById('theme-btn');
  if (btn) btn.textContent = THEME_LABELS[theme] || '☀ Light';
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
  const role = document.getElementById('hero-role');
  const first = document.getElementById('hero-firstname');
  const last = document.getElementById('hero-lastname');
  if (role)  role.textContent  = '\u2726 ' + about.tagline;
  if (first) first.textContent = about.name.split(' ')[0];
  if (last)  last.textContent  = about.name.split(' ').slice(-1)[0] + '.';
}

/* ============================================================
   MAIN
   ============================================================ */
async function init() {
  initTheme();
  initScrollReveal();

  const needsAbout    = document.getElementById('hero-firstname') || document.getElementById('about-bio');
  const needsFacts    = document.getElementById('facts-grid');
  const needsProjects = document.getElementById('projects-grid');
  const needsBooks    = document.getElementById('books-shelf');
  const needsSongs    = document.getElementById('songs-mine');
  const needsSkills   = document.getElementById('skills-grid');

  const [about, facts, projects, books, songs, skills] = await Promise.all([
    needsAbout    ? api('/about').catch(() => null)                              : Promise.resolve(null),
    needsFacts    ? api('/fun-fact/all').catch(() => [])                         : Promise.resolve([]),
    needsProjects ? api('/projects').catch(() => [])                             : Promise.resolve([]),
    needsBooks    ? api('/books').catch(() => ({ mine: [], community: [] }))     : Promise.resolve({ mine: [], community: [] }),
    needsSongs    ? api('/songs').catch(() => ({ mine: [], community: [] }))     : Promise.resolve({ mine: [], community: [] }),
    needsSkills   ? api('/skills').catch(() => [])                               : Promise.resolve([]),
  ]);

  if (about) {
    initHero(about);
    initAbout(about);
    const landingBio = document.getElementById('landing-bio');
    if (landingBio) landingBio.textContent = about.bio;
  }
  if (needsFacts)    initFunFacts(facts);
  if (needsProjects) initProjects(projects);
  if (needsBooks)  { initBooks(books); initBooksForm(); }
  if (needsSongs)  { initSongs(songs); initSongsForm(); }
  if (needsSkills)   initSkills(skills);

  initGame();
  initContact();
  initPageNext();
}

/* ============================================================
   STUBS — sections not yet implemented
   ============================================================ */
function initAbout(about) {
  const bio = document.getElementById('about-bio');
  if (!bio) return;
  bio.textContent = about.bio;
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
function initSkills(skills) {
  const grid = document.getElementById('skills-grid');
  if (!grid || !skills.length) return;
  skills.forEach(group => {
    const block = document.createElement('div');
    block.className = 'skill-block';
    const rows = group.items.map(s => {
      const dots = [1,2,3].map(i =>
        `<i class="ldot${i <= s.level ? ' ldot-on' : ''}"></i>`
      ).join('');
      return `
        <div class="skill-row">
          <span class="skill-name">${s.name}</span>
          <span class="skill-dots">${dots}</span>
        </div>`;
    }).join('');
    block.innerHTML = `
      <div class="skill-block-header">
        <span class="skill-block-icon">${group.icon}</span>
        <span class="skill-block-label">${group.category}</span>
      </div>
      <div class="skill-rows">${rows}</div>
    `;
    grid.appendChild(block);
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
    <div class="proj-screens proj-screens-2up">
      <div class="proj-screen-phone">
        <img src="https://amanda-portfolio-assets.s3.amazonaws.com/farmcare-landing.png" alt="FarmCare landing screen">
      </div>
      <div class="proj-screen-phone">
        <img src="https://amanda-portfolio-assets.s3.amazonaws.com/farmcare-animals.png" alt="FarmCare animals screen">
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
  const grid  = document.getElementById('facts-grid');
  const count = document.getElementById('ff-count');
  const total = document.getElementById('ff-total');

  total.textContent = facts.length;
  let revealed = 0;

  facts.forEach(f => {
    const card = document.createElement('div');
    card.className = 'scratch-card';
    card.innerHTML = `
      <div class="scratch-content">
        <div class="fact-num">#${String(f.id).padStart(2, '0')}</div>
        <p class="fact-text">${f.fact}</p>
      </div>
    `;

    const canvas = document.createElement('canvas');
    canvas.className = 'scratch-overlay';
    card.appendChild(canvas);
    grid.appendChild(card);

    // Size canvas to card after DOM insert
    requestAnimationFrame(() => {
      canvas.width  = card.offsetWidth  || 260;
      canvas.height = card.offsetHeight || 160;
      drawScratchSurface(canvas);
    });

    makeScratchable(canvas, () => {
      revealed++;
      count.textContent = revealed;
      if (revealed === facts.length) {
        setTimeout(() => showToast('You know everything about me now 👀'), 400);
      }
    });
  });
}

function drawScratchSurface(canvas) {
  const ctx = canvas.getContext('2d');
  const grad = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
  grad.addColorStop(0, '#5A3A8A');
  grad.addColorStop(0.5, '#8A5AAA');
  grad.addColorStop(1, '#5A3A8A');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Subtle noise texture
  ctx.fillStyle = 'rgba(255,255,255,0.04)';
  for (let i = 0; i < 80; i++) {
    const x = Math.random() * canvas.width;
    const y = Math.random() * canvas.height;
    ctx.fillRect(x, y, Math.random() * 3 + 1, Math.random() * 3 + 1);
  }

  ctx.fillStyle = 'rgba(255,255,255,0.45)';
  ctx.font = '600 11px DM Sans, sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('✦ scratch to reveal ✦', canvas.width / 2, canvas.height / 2);
}

function makeScratchable(canvas, onReveal) {
  const ctx = canvas.getContext('2d');
  let scratching = false;
  let done = false;

  function getXY(e) {
    const rect = canvas.getBoundingClientRect();
    const src  = e.touches ? e.touches[0] : e;
    return [
      (src.clientX - rect.left) * (canvas.width  / rect.width),
      (src.clientY - rect.top)  * (canvas.height / rect.height)
    ];
  }

  function scratch(x, y) {
    ctx.globalCompositeOperation = 'destination-out';
    ctx.beginPath();
    ctx.arc(x, y, 55, 0, Math.PI * 2);
    ctx.fill();
    checkDone();
  }

  function checkDone() {
    if (done) return;
    const data = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
    let transparent = 0;
    for (let i = 3; i < data.length; i += 4) if (data[i] < 128) transparent++;
    if (transparent / (canvas.width * canvas.height) > 0.3) {
      done = true;
      canvas.style.opacity = '0';
      setTimeout(() => { canvas.style.display = 'none'; onReveal(); }, 500);
    }
  }

  canvas.addEventListener('mousedown',  e => { scratching = true;  scratch(...getXY(e)); });
  canvas.addEventListener('mousemove',  e => { if (scratching) scratch(...getXY(e)); });
  canvas.addEventListener('mouseup',    () => scratching = false);
  canvas.addEventListener('mouseleave', () => scratching = false);
  canvas.addEventListener('touchstart', e => { e.preventDefault(); scratching = true;  scratch(...getXY(e)); }, { passive: false });
  canvas.addEventListener('touchmove',  e => { e.preventDefault(); if (scratching) scratch(...getXY(e)); }, { passive: false });
  canvas.addEventListener('touchend',   () => scratching = false);
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


/* ============================================================
   GAME — This or That
   ============================================================ */
const GAME_QUESTIONS = [
  { q: 'When it comes to coding…',       a: 'Code first',      b: 'Plan first',       answer: 'b', why: "I like to know where I'm going before I start. Plan first, then build with confidence." },
  { q: 'My natural timezone is…',        a: 'Night owl 🦉',    b: 'Early bird ☀️',    answer: 'a', why: "2am is when the best ideas hit. Morning me is not to be trusted." },
  { q: 'When a bug appears I…',          a: 'Fix it obsessively', b: 'Walk away & come back', answer: 'b', why: "Step away, make tea, come back — it's always obvious after." },
  { q: 'My default setting is…',         a: 'Headphones in 🎧', b: 'Ambient noise',   answer: 'a', why: "Headphones in = do not disturb. It's a lifestyle." },
  { q: 'I thrive with…',                 a: 'Structure & plans', b: 'Vibes & momentum', answer: 'b', why: "Plans are just vibes with extra steps. I move on momentum." },
];

let tq = { round: 0, score: 0, timer: null, answers: [] };

function initGame() {
  const wrap = document.getElementById('game-wrap');
  if (!wrap) return;
  renderTTIntro();
}

function renderTTIntro() {
  const wrap = document.getElementById('game-wrap');
  wrap.innerHTML = `
    <div class="game-intro">
      <p><strong>${GAME_QUESTIONS.length} questions. 4 seconds each.</strong><br>Pick what <strong>you</strong> would do — no right or wrong answers.<br>At the end I’ll reveal what I’d pick and we’ll see how alike we are.</p>
      <button class="game-play-btn" onclick="startTT()">Start &rarr;</button>
    </div>
  `;
}

function startTT() {
  tq = { round: 0, score: 0, timer: null, answers: [] };
  renderTTRound();
}

function renderTTRound() {
  clearInterval(tq.timer);
  const wrap = document.getElementById('game-wrap');
  const q = GAME_QUESTIONS[tq.round];
  let timeLeft = 4;
  let picked = false;

  wrap.innerHTML = `
    <div class="tt-progress">
      <div class="tt-progress-fill" id="tt-prog"></div>
    </div>
    <div class="tt-round-label">Question ${tq.round + 1} of ${GAME_QUESTIONS.length}</div>
    <div class="tt-question">${q.q}</div>
    <div class="tt-panels">
      <button class="tt-panel" id="tt-a"><span>${q.a}</span></button>
      <div class="tt-or">or</div>
      <button class="tt-panel" id="tt-b"><span>${q.b}</span></button>
    </div>
    <div class="tt-timer-text" id="tt-timer">${timeLeft}s</div>
  `;

  document.getElementById('tt-a').addEventListener('click', () => pick('a'));
  document.getElementById('tt-b').addEventListener('click', () => pick('b'));

  // Animate progress bar depletion
  requestAnimationFrame(() => requestAnimationFrame(() => {
    const bar = document.getElementById('tt-prog');
    if (bar) { bar.style.transition = `width ${timeLeft}s linear`; bar.style.width = '0%'; }
  }));

  tq.timer = setInterval(() => {
    timeLeft--;
    const el = document.getElementById('tt-timer');
    if (el) el.textContent = timeLeft + 's';
    if (timeLeft <= 0) { clearInterval(tq.timer); pick(null); }
  }, 1000);

  function pick(choice) {
    if (picked) return;
    picked = true;
    clearInterval(tq.timer);

    const correct = choice === q.answer;
    if (correct) tq.score++;
    tq.answers.push({ picked: choice, correct, q });

    const panelA = document.getElementById('tt-a');
    const panelB = document.getElementById('tt-b');
    if (panelA && panelB) {
      panelA.disabled = true;
      panelB.disabled = true;
      if (choice === 'a') panelA.classList.add(correct ? 'tt-correct' : 'tt-wrong');
      if (choice === 'b') panelB.classList.add(correct ? 'tt-correct' : 'tt-wrong');
      if (q.answer === 'a') panelA.classList.add('tt-correct');
      if (q.answer === 'b') panelB.classList.add('tt-correct');
    }

    tq.round++;
    setTimeout(() => {
      if (tq.round < GAME_QUESTIONS.length) renderTTRound();
      else renderTTResult();
    }, 900);
  }
}

function renderTTResult() {
  const wrap = document.getElementById('game-wrap');
  const pct  = Math.round((tq.score / GAME_QUESTIONS.length) * 100);
  const msgs = [
    { min: 100, title: 'We are literally the same person 😭', sub: "Same chaos, same energy, same everything. Concerning but fun." },
    { min: 80,  title: 'Very similar energy',           sub: "We think alike. We’d probably vibe on a project together." },
    { min: 60,  title: 'More in common than expected',  sub: "We overlap where it counts. I’d work with you." },
    { min: 40,  title: "Opposites in some ways",        sub: "Different approaches — and honestly that’s interesting. Reach out anyway." },
    { min: 0,   title: "We are very different people",  sub: "And that's fine. The best teams aren't made of clones." },
  ];
  const msg = msgs.find(m => pct >= m.min);

  const rows = tq.answers.map((a, i) => {
    const q = GAME_QUESTIONS[i];
    const match = a.picked === q.answer;
    const icon = match ? '✓' : '·';
    const cls  = match ? 'tt-res-correct' : 'tt-res-wrong';
    const yourPick   = a.picked ? (a.picked === 'a' ? q.a : q.b) : 'ran out of time';
    const amandaPick = q.answer === 'a' ? q.a : q.b;
    return `
      <div class="tt-res-row ${cls}">
        <span class="tt-res-icon">${icon}</span>
        <div>
          <div class="tt-res-q">${q.q}</div>
          <div class="tt-res-detail">You: <strong>${yourPick}</strong> · Me: <strong>${amandaPick}</strong></div>
          <div class="tt-res-why">"${q.why}"</div>
        </div>
      </div>
    `;
  }).join('');

  wrap.innerHTML = `
    <div class="tt-result">
      <div class="tt-result-score">${pct}<span>% match</span></div>
      <div class="tt-result-title">${msg.title}</div>
      <p class="tt-result-sub">${msg.sub}</p>
      <div class="tt-res-list">${rows}</div>
      <button class="game-replay-btn" onclick="startTT()">Play again &rarr;</button>
    </div>
  `;
}

/* ============================================================
   PAGE NEXT NAVIGATION
   ============================================================ */
const PAGE_SEQUENCE = [
  { path: '/',          label: 'Home' },
  { path: '/about',     label: 'About' },
  { path: '/journey',   label: 'Journey' },
  { path: '/skills',    label: 'Skills' },
  { path: '/fun-facts', label: 'Fun Facts' },
  { path: '/projects',  label: 'Projects' },
  { path: '/books',     label: 'Books' },
  { path: '/songs',     label: 'Songs' },
  { path: '/play',      label: 'Play' },
  { path: '/contact',   label: null },
];

function initPageNext() {
  const current = window.location.pathname.replace(/\/$/, '') || '/';
  const idx = PAGE_SEQUENCE.findIndex(p => p.path === current || (current === '' && p.path === '/'));
  if (idx === -1 || idx === PAGE_SEQUENCE.length - 1) return;
  const next = PAGE_SEQUENCE[idx + 1];
  const wrap = document.getElementById('page-next');
  const link = document.getElementById('page-next-link');
  const lbl  = document.getElementById('page-next-label');
  if (!wrap || !link || !lbl) return;
  lbl.textContent = 'Next: ' + next.label;
  link.href = PAGE_SEQUENCE[idx + 1].path;
  wrap.style.display = 'flex';
}

document.addEventListener('DOMContentLoaded', init);

/* ============================================================
   EASTER EGG
   ============================================================ */
console.log(
  '%c✦ Hey, you found the console. %c\nBuilt with Flask + vanilla JS, deployed on AWS Lambda.\nSee the source: https://github.com/AmandaSoganile/portfolio-website',
  'color:#7B52A0;font-size:14px;font-weight:700;',
  'color:#aaa;font-size:12px;'
);
