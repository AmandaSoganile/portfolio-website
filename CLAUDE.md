# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Personal portfolio website for Amanda Songanile. Flask + vanilla JS, multi-page architecture, deployed to AWS Lambda via GitHub Actions.

## Current Stack

- Flask (Python) — templates, API routes
- Vanilla JS — theme cycling, API calls, scroll reveal
- SQLite — data storage (portfolio.db locally, /tmp/portfolio.db on Lambda)
- S3 bucket: `amanda-portfolio-assets` — static image hosting
- Deployed: API Gateway v2 (kmn5hw7375) → Lambda (amanda-portfolio) in us-east-1
- CI/CD: push to `prod` branch triggers `.github/workflows/deploy.yml`

## Pages

| Route | Template |
|-------|----------|
| `/` | `templates/landing.html` |
| `/about` | `templates/about.html` |
| `/journey` | `templates/journey.html` |
| `/skills` | `templates/skills.html` |
| `/projects` | `templates/projects.html` |
| `/fun-facts` | `templates/fun-facts.html` |
| `/books` | `templates/books.html` |
| `/songs` | `templates/songs.html` |
| `/play` | `templates/play.html` |
| `/contact` | `templates/contact.html` |

## Architecture

- `app.py` — Flask app, all blueprints registered with `url_prefix='/api'`
- `routes/frontend.py` — page routes
- `routes/about.py` — /api/about, /api/skills
- `data/` — JSON data files (projects.json, skills.json, songs_mine.json, etc.)
- `static/css/style.css` — all styles, cache-busted with `?v=N`
- `static/js/app.js` — all JS, cache-busted with `?v=N`
- `templates/base.html` — shared nav, theme button, page-next pill, footer

## Theming

Three themes cycled via button: `dark` → `light` → `pink`
- `:root` (light): `--bg: #F5F4F2; --bg2: #EDECE9; --card: #F9F8F6`
- `[data-theme="dark"]`: `--bg: #07070F; --bg2: #0D0D1A; --card: #11111E`
- `[data-theme="pink"]`: `--bg: #FDF0F4; --bg2: #F8E4EB; --card: #FFF5F8`
- Saved to `localStorage` under key `portfolio-theme`
- Theme button labels: dark→"☀ Light", light→"🌸 Pink", pink→"◑ Dark"

## Photo

Real photo at `https://amanda-portfolio-assets.s3.amazonaws.com/amanda.jpg`
Scrapbook effect: white border (`border: 6px solid #fff`), `.photo-tape` div above, `.sticky-note` below.

## Cache Busting

Current version: `v=26`. Bump in `templates/base.html` whenever CSS or JS changes.

## Key Decisions

- Lambda filesystem read-only → SQLite at `/tmp/portfolio.db` on Lambda, local path otherwise
- All API routes prefixed `/api/`
- `initHero()` is null-safe — hero elements don't exist on all pages
- PAGE_SEQUENCE in app.js drives the "Next: X →" pill navigation

## Email (SES)

Contact form POSTs to `/api/contact`. On Lambda, `_send_via_ses()` in `routes/contact.py` sends via SES.
- Sender and recipient: `CONTACT_EMAIL` env var (default: soganileamanda@gmail.com)
- SES region: us-east-1
- Lambda IAM role needs `ses:SendEmail` on `arn:aws:ses:us-east-1:*:identity/soganileamanda@gmail.com`
- boto3 is pre-installed on Lambda — not in deploy package, not needed locally
- Falls back to CloudWatch logging if SES fails (does not surface error to visitor)

## Admin Portal

- Route: `/admin` (login), `/admin/dashboard`
- Auth: password-only via `ADMIN_PASSWORD` env var; `SECRET_KEY` env var for session signing
- Blueprint: `routes/admin.py`, templates in `templates/admin/`
- Features: manage book/song submissions (show/hide/delete), read/delete contact messages, edit all 6 JSON data files in `data/`
- JSON edits only persist locally — Lambda filesystem is read-only, so redeploy to apply data changes

## Change History

| Date | File | What Changed |
|------|------|-------------|
| 2026-04-07 | `static/css/style.css` | Light theme bg changed from cream (#ECEAE2) to off-white (#F5F4F2); card from #F2EEE6 to #F9F8F6 |
| 2026-04-07 | `templates/base.html` | Cache-bust version bumped to v=26 |
| 2026-04-07 | `routes/contact.py` | Wired SES email sending via `_send_via_ses()`; falls back to log on failure |
| 2026-04-08 | `store.py` | Added `visible` column to submissions tables, `contact_messages` table, admin CRUD methods |
| 2026-04-08 | `routes/admin.py` | New admin blueprint: login, dashboard, submissions management, JSON data file editor |
| 2026-04-08 | `routes/contact.py` | Save incoming messages to `contact_messages` DB table |
| 2026-04-08 | `app.py` | Registered admin blueprint; added `SECRET_KEY` and `ADMIN_PASSWORD` config |
