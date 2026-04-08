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
                submitted_at TEXT NOT NULL,
                visible      INTEGER NOT NULL DEFAULT 1
            );
            CREATE TABLE IF NOT EXISTS song_submissions (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                name         TEXT NOT NULL,
                title        TEXT NOT NULL,
                artist       TEXT NOT NULL DEFAULT '',
                note         TEXT NOT NULL DEFAULT '',
                submitted_at TEXT NOT NULL,
                visible      INTEGER NOT NULL DEFAULT 1
            );
            CREATE TABLE IF NOT EXISTS contact_messages (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL,
                email       TEXT NOT NULL,
                message     TEXT NOT NULL,
                received_at TEXT NOT NULL
            );
        """)
        # Migrate pre-existing tables that may lack the visible column
        for table in ("book_submissions", "song_submissions"):
            try:
                self._db.execute(
                    f"ALTER TABLE {table} ADD COLUMN visible INTEGER NOT NULL DEFAULT 1"
                )
                self._db.commit()
            except sqlite3.OperationalError:
                pass  # column already present
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
            "INSERT INTO book_submissions (name, title, author, submitted_at, visible) VALUES (?, ?, ?, ?, 1)",
            (name, title, author, date.today().isoformat())
        )
        self._db.commit()

    def get_book_submissions(self) -> list:
        """Public — visible only, no id."""
        rows = self._db.execute(
            "SELECT name, title, author, submitted_at FROM book_submissions WHERE visible = 1 ORDER BY id ASC"
        ).fetchall()
        return [dict(row) for row in rows]

    def get_all_books(self) -> list:
        """Admin — all rows with id and visible flag."""
        rows = self._db.execute(
            "SELECT id, name, title, author, submitted_at, visible FROM book_submissions ORDER BY id ASC"
        ).fetchall()
        return [dict(row) for row in rows]

    def toggle_book_visible(self, row_id: int) -> None:
        self._db.execute(
            "UPDATE book_submissions SET visible = 1 - visible WHERE id = ?", (row_id,)
        )
        self._db.commit()

    def delete_book(self, row_id: int) -> None:
        self._db.execute("DELETE FROM book_submissions WHERE id = ?", (row_id,))
        self._db.commit()

    # --- Songs ---

    def add_song(self, name: str, title: str, artist: str = "", note: str = "") -> None:
        from datetime import date
        self._db.execute(
            "INSERT INTO song_submissions (name, title, artist, note, submitted_at, visible) VALUES (?, ?, ?, ?, ?, 1)",
            (name, title, artist, note, date.today().isoformat())
        )
        self._db.commit()

    def get_song_submissions(self) -> list:
        """Public — visible only, no id."""
        rows = self._db.execute(
            "SELECT name, title, artist, note, submitted_at FROM song_submissions WHERE visible = 1 ORDER BY id ASC"
        ).fetchall()
        return [dict(row) for row in rows]

    def get_all_songs(self) -> list:
        """Admin — all rows with id and visible flag."""
        rows = self._db.execute(
            "SELECT id, name, title, artist, note, submitted_at, visible FROM song_submissions ORDER BY id ASC"
        ).fetchall()
        return [dict(row) for row in rows]

    def toggle_song_visible(self, row_id: int) -> None:
        self._db.execute(
            "UPDATE song_submissions SET visible = 1 - visible WHERE id = ?", (row_id,)
        )
        self._db.commit()

    def delete_song(self, row_id: int) -> None:
        self._db.execute("DELETE FROM song_submissions WHERE id = ?", (row_id,))
        self._db.commit()

    # --- Contact Messages ---

    def add_contact_message(self, name: str, email: str, message: str) -> None:
        from datetime import datetime, timezone
        self._db.execute(
            "INSERT INTO contact_messages (name, email, message, received_at) VALUES (?, ?, ?, ?)",
            (name, email, message, datetime.now(timezone.utc).isoformat())
        )
        self._db.commit()

    def get_contact_messages(self) -> list:
        rows = self._db.execute(
            "SELECT id, name, email, message, received_at FROM contact_messages ORDER BY id DESC"
        ).fetchall()
        return [dict(row) for row in rows]

    def delete_contact_message(self, row_id: int) -> None:
        self._db.execute("DELETE FROM contact_messages WHERE id = ?", (row_id,))
        self._db.commit()
