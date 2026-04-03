import sqlite3


class Store:
    def __init__(self, db_path: str):
        self._db = sqlite3.connect(db_path, check_same_thread=False)
        self._db.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        self._db.executescript("""
            CREATE TABLE IF NOT EXISTS reactions (
                fact_id   INTEGER NOT NULL,
                emoji     TEXT    NOT NULL,
                count     INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (fact_id, emoji)
            );
            CREATE TABLE IF NOT EXISTS book_submissions (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                name         TEXT NOT NULL,
                title        TEXT NOT NULL,
                author       TEXT NOT NULL DEFAULT '',
                submitted_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS song_submissions (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                name         TEXT NOT NULL,
                title        TEXT NOT NULL,
                artist       TEXT NOT NULL DEFAULT '',
                note         TEXT NOT NULL DEFAULT '',
                submitted_at TEXT NOT NULL
            );
        """)
        self._db.commit()

    # --- Reactions ---

    def add_reaction(self, fact_id: int, emoji: str) -> dict:
        self._db.execute("""
            INSERT INTO reactions (fact_id, emoji, count) VALUES (?, ?, 1)
            ON CONFLICT(fact_id, emoji) DO UPDATE SET count = count + 1
        """, (fact_id, emoji))
        self._db.commit()
        return self.get_reactions(fact_id)

    def get_reactions(self, fact_id: int) -> dict:
        rows = self._db.execute(
            "SELECT emoji, count FROM reactions WHERE fact_id = ?", (fact_id,)
        ).fetchall()
        return {row["emoji"]: row["count"] for row in rows}

    # --- Books ---

    def add_book(self, name: str, title: str, author: str = "") -> None:
        from datetime import date
        self._db.execute(
            "INSERT INTO book_submissions (name, title, author, submitted_at) VALUES (?, ?, ?, ?)",
            (name, title, author, date.today().isoformat())
        )
        self._db.commit()

    def get_book_submissions(self) -> list:
        rows = self._db.execute(
            "SELECT name, title, author, submitted_at FROM book_submissions ORDER BY id ASC"
        ).fetchall()
        return [dict(row) for row in rows]

    # --- Songs ---

    def add_song(self, name: str, title: str, artist: str = "", note: str = "") -> None:
        from datetime import date
        self._db.execute(
            "INSERT INTO song_submissions (name, title, artist, note, submitted_at) VALUES (?, ?, ?, ?, ?)",
            (name, title, artist, note, date.today().isoformat())
        )
        self._db.commit()

    def get_song_submissions(self) -> list:
        rows = self._db.execute(
            "SELECT name, title, artist, note, submitted_at FROM song_submissions ORDER BY id ASC"
        ).fetchall()
        return [dict(row) for row in rows]
