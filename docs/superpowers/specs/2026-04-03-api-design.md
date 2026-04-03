# API Design Spec — Amanda Soganile Portfolio
**Date:** 2026-04-03
**Version:** 0.1.0

---

## Overview

API-first Flask portfolio site. The frontend fetches all content from the backend — nothing is hardcoded in HTML. Designed to run locally during development and deploy to AWS Lambda in production.

---

## Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/meta` | Version, git SHA, deploy timestamp, environment |
| GET | `/about` | Bio, personal details, mission, currently learning |
| GET | `/projects` | Project list (FarmCare) |
| GET | `/fun-fact/all` | All 10 fun facts with current reaction counts |
| POST | `/fun-fact/<id>/react` | Add an emoji reaction to a specific fun fact |
| GET | `/fun-fact/<id>/reactions` | Get reaction counts for a specific fun fact |
| GET | `/books` | Amanda's books + visitor submissions |
| POST | `/books` | Visitor submits a book: name + title |
| GET | `/songs` | Amanda's songs + visitor submissions (MJ fun fact) |
| POST | `/songs` | Visitor submits a song: name + title + note |
| POST | `/contact` | Contact form → email notification to Amanda |

---

## Response Shapes

### GET /meta
```json
{
  "version": "0.1.0",
  "deployed_at": "2026-04-03T10:00:00+00:00",
  "commit_sha": "a1b2c3d",
  "environment": "development"
}
```

### GET /about
```json
{
  "name": "Amanda Fezile Soganile",
  "name_meaning": "Fezile is a Ndebele name meaning 'A wish that has come true'",
  "tagline": "Integration Engineering Intern",
  "location": "Victoria Falls, Zimbabwe",
  "birthday": "17 September",
  "bio": "Hi, I'm Amanda...",
  "things_i_love": ["flowers", "the night sky", "the moon", "sunsets and sunrises"],
  "things_ill_never_shut_up_about": ["food"],
  "quirky_talent": "...",
  "what_drives_me": "...",
  "what_i_care_about": "...",
  "life_goal": "Peaceful and happy.",
  "currently_learning": ["AWS Lambda", "Flask", "CI/CD pipelines", "GitHub Actions", "API design"],
  "mission": "To build things that matter, keep learning relentlessly, and never just exist."
}
```

### GET /fun-fact/all
```json
[
  {
    "id": 1,
    "fact": "I still hate vegetables and I'm almost 21 years old.",
    "reactions": { "😂": 4, "💀": 2, "😭": 1 }
  }
]
```

### GET /fun-fact/<id>/reactions
```json
{ "fact_id": 1, "reactions": { "😂": 4, "💀": 2, "😭": 1 } }
```

### POST /fun-fact/<id>/react
Request:
```json
{ "emoji": "😂" }
```
Response:
```json
{ "status": "ok", "reactions": { "😂": 5, "💀": 2 } }
```

Allowed emojis: `😂`, `💀`, `😭`, `🫶`, `👀`

### GET /books
```json
{
  "mine": [
    { "title": "Atomic Habits", "author": "James Clear" },
    { "title": "101 Essays That Will Change the Way You Think", "author": "Brianna Wiest" },
    { "title": "Ego Is the Enemy", "author": "Ryan Holiday" },
    { "title": "How to Win Friends & Influence People", "author": "Dale Carnegie" },
    { "title": "Thinking, Fast and Slow", "author": "Daniel Kahneman" },
    { "title": "Rich Dad Poor Dad", "author": "Robert T. Kiyosaki" },
    { "title": "Getting Things Done", "author": "David Allen" }
  ],
  "community": [
    {
      "name": "Thabo",
      "title": "The Subtle Art of Not Giving a F*ck",
      "author": "Mark Manson",
      "submitted_at": "2026-04-03"
    }
  ]
}
```

### POST /books
Request:
```json
{ "name": "Thabo", "title": "Atomic Habits" }
```
Response:
```json
{ "status": "ok", "message": "Book added!" }
```

Author is not required from the visitor — if omitted it is stored as an empty string.

### GET /songs
```json
{
  "mine": [
    { "title": "Billie Jean", "artist": "Michael Jackson" },
    { "title": "Thriller", "artist": "Michael Jackson" },
    { "title": "Human Nature", "artist": "Michael Jackson" },
    { "title": "Rock With You", "artist": "Michael Jackson" },
    { "title": "Man in the Mirror", "artist": "Michael Jackson" }
  ],
  "community": [
    {
      "name": "Lerato",
      "title": "Human Nature",
      "artist": "Michael Jackson",
      "note": "This one hits different at 2am",
      "submitted_at": "2026-04-03"
    }
  ]
}
```

### POST /songs
Request:
```json
{ "name": "Lerato", "title": "Human Nature", "artist": "Michael Jackson", "note": "This one hits different at 2am" }
```
Response:
```json
{ "status": "ok", "message": "Song added!" }
```

### POST /contact
Request:
```json
{ "name": "Thabo", "slack_email": "thabo@company.slack.com", "message": "Love your work, let's connect!" }
```
Response:
```json
{ "status": "ok", "message": "Thanks! I'll get back to you soon." }
```
Sends a casual email notification to Amanda's address (set via `CONTACT_EMAIL` env var).

---

## Storage

### Local Development — SQLite
Single file: `portfolio.db`

**Tables:**
- `reactions(id, fact_id, emoji, count)` — tracks emoji counts per fun fact
- `book_submissions(id, name, title, author, submitted_at)`
- `song_submissions(id, name, title, artist, note, submitted_at)`

Seed/static data (Amanda's own books, songs, about info) stays in JSON flat files — only visitor-submitted content goes in the DB.

### Production — DynamoDB
Same three tables as DynamoDB tables. Accessed through a `store.py` abstraction layer so Flask routes are identical in both environments.

Storage backend is selected via environment variable:
```
STORAGE_BACKEND=sqlite   # default, local dev
STORAGE_BACKEND=dynamodb # production
```

### Static Data Files
```
data/
  about.json
  fun_facts.json
  projects.json
  books_mine.json
  songs_mine.json
```

---

## Email (Contact Form)

- **Local dev:** prints message to console, no real email sent
- **Production:** AWS SES — sends to `CONTACT_EMAIL` env var
- Message format: casual, e.g. "hey amanda, Thabo wants to chat — thabo@company.slack.com says: [message]"

---

## Environment Variables

```
FLASK_ENV=development
STORAGE_BACKEND=sqlite
CONTACT_EMAIL=               # Amanda's email address
GIT_SHA=                     # stamped at deploy time
DEPLOY_TIMESTAMP=            # stamped at deploy time
AWS_REGION=                  # production only
DYNAMODB_TABLE_PREFIX=       # production only
SES_SENDER_EMAIL=            # production only
```

---

## What's Out of Scope (for now)

- AWS deployment (Lambda, API Gateway, DynamoDB) — Phase 2
- GitHub Actions CI/CD — Phase 2
- Frontend HTML/CSS/JS — Phase 3
- Authentication / admin view — not planned
