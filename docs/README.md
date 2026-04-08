# Portfolio Website — Docs

## Recent Changes

### 2026-04-08 — Admin portal

Added a password-protected admin portal at `/admin`.

**Login:** password-only. Set the `ADMIN_PASSWORD` environment variable to your chosen password. Also set `SECRET_KEY` to a random string for session signing (especially important on Lambda).

**Dashboard tabs:**
- **Books** — view all community book submissions, toggle visibility (show/hide from public site), or delete permanently
- **Songs** — same as Books
- **Messages** — read all contact form submissions (stored to DB on submit), delete when done
- **Data Files** — edit `about.json`, `fun_facts.json`, `projects.json`, `skills.json`, `books_mine.json`, `songs_mine.json` in-browser with JSON validation before save. On Lambda the filesystem is read-only — edit locally and redeploy.

**Files changed:**
- `store.py` — `visible` column on submissions, `contact_messages` table, admin CRUD methods
- `routes/admin.py` — new blueprint (login, dashboard, all actions)
- `routes/contact.py` — saves each submission to `contact_messages`
- `app.py` — registers admin blueprint, `SECRET_KEY` + `ADMIN_PASSWORD` config

### 2026-04-07 — Light theme background update

Updated `static/css/style.css` `:root` variables so the light theme uses a soft off-white instead of the warmer cream tones.

| Variable | Before | After |
|----------|--------|-------|
| `--bg` | `#ECEAE2` | `#F5F4F2` |
| `--bg2` | `#E2DDD5` | `#EDECE9` |
| `--card` | `#F2EEE6` | `#F9F8F6` |

Cache-bust version bumped to `v=26` in `templates/base.html`.
