# Amanda Soganile — Portfolio Website

Personal portfolio website built with Flask and vanilla JS.

## Stack

| Layer | Tech |
|-------|------|
| Backend | Python / Flask |
| Frontend | HTML, CSS, Vanilla JS |
| Database | SQLite |
| Fonts | Playfair Display + DM Sans (Google Fonts) |

## Running locally

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python3 -c "from app import create_app; create_app().run(debug=False, port=5002)"
```

Then open `http://127.0.0.1:5002`.

## Project structure

```
├── app.py               # Flask app factory
├── store.py             # SQLite data layer
├── routes/              # API blueprints
│   ├── about.py         # GET /about, GET /projects
│   ├── fun_facts.py     # GET /fun-fact/all, POST reactions
│   ├── books.py         # GET/POST /books
│   ├── songs.py         # GET/POST /songs
│   ├── contact.py       # POST /contact
│   └── frontend.py      # Serves index.html
├── templates/
│   └── index.html       # Single-page frontend
├── static/
│   ├── css/style.css
│   └── js/app.js
├── data/                # Seed JSON files
└── tests/               # pytest test suite
```

## Sections

- **Hero** — name, role, photo frame, social links
- **About** — bio, name meaning, things I love, life goal
- **Journey** — personal timeline milestones
- **Fun Facts** — community reaction cards
- **Projects** — FarmCare (Swift/iOS)
- **Books** — bookshelf with cover popups + community recs
- **Songs** — playlist + community recommendations
- **Contact** — message form

## API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/about` | Bio, tags, name meaning |
| GET | `/projects` | Project list |
| GET | `/fun-fact/all` | All fun facts |
| POST | `/fun-fact/:id/react` | Add reaction |
| GET | `/books` | Books (mine + community) |
| POST | `/books` | Add community book |
| GET | `/songs` | Songs (mine + community) |
| POST | `/songs` | Add community song |
| POST | `/contact` | Send message |
