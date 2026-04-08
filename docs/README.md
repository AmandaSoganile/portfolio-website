# Portfolio Website — Docs

## Recent Changes

### 2026-04-08 — Visitor tracking on admin dashboard

Added page-view tracking with IP geolocation. Every frontend page load records the path, timestamp, and visitor location (country, city, region) via ip-api.com. Raw IPs are never stored — only a SHA-256 hash prefix for unique-visitor counting.

**Admin dashboard changes:**
- Three stat cards at the top: Unique Visitors, Page Views, Messages
- New "Visitors" tab (default): location breakdown table + last 50 recent visits
- Geo lookup only runs once per new visitor (cached for repeat visits), with a 1s timeout so it never blocks page loads

**Files changed:**
- `store.py` — `page_views` table, methods for recording views and querying stats/locations
- `app.py` — `_geolocate_ip()` helper, `before_request` hook that tracks frontend routes
- `routes/admin.py` — passes `visitor_stats`, `visitor_locations`, `recent_visits` to dashboard
- `templates/admin/dashboard.html` — stat cards, Visitors tab with location + recent-visits tables

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
