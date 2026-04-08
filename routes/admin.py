import hmac
import json
from functools import wraps
from pathlib import Path

from flask import (
    Blueprint, current_app, redirect, render_template,
    request, session, url_for,
)

bp = Blueprint("admin", __name__, url_prefix="/admin")

DATA = Path(__file__).parent.parent / "data"

EDITABLE_FILES = [
    "about.json",
    "fun_facts.json",
    "projects.json",
    "skills.json",
    "books_mine.json",
    "songs_mine.json",
]


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return decorated


def _load_files() -> dict:
    files = {}
    for fname in EDITABLE_FILES:
        try:
            raw = (DATA / fname).read_text()
            files[fname] = json.dumps(json.loads(raw), indent=2)
        except (FileNotFoundError, json.JSONDecodeError):
            files[fname] = ""
    return files


def _dashboard_ctx(store, **extra) -> dict:
    return dict(
        books=store.get_all_books(),
        songs=store.get_all_songs(),
        messages=store.get_contact_messages(),
        files=_load_files(),
        editable_files=EDITABLE_FILES,
        **extra,
    )


# ---------------------------------------------------------------------------

@bp.route("/")
def index():
    if session.get("admin"):
        return redirect(url_for("admin.dashboard"))
    return redirect(url_for("admin.login"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        entered = request.form.get("password", "")
        stored = current_app.config.get("ADMIN_PASSWORD", "")
        if stored and hmac.compare_digest(entered, stored):
            session["admin"] = True
            return redirect(url_for("admin.dashboard"))
        error = "Incorrect password."
    return render_template("admin/login.html", error=error)


@bp.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("admin.login"))


@bp.route("/dashboard")
@login_required
def dashboard():
    from app import get_store
    return render_template("admin/dashboard.html", **_dashboard_ctx(get_store()))


# --- Book actions ---

@bp.route("/books/<int:row_id>/toggle", methods=["POST"])
@login_required
def toggle_book(row_id):
    from app import get_store
    get_store().toggle_book_visible(row_id)
    return redirect(url_for("admin.dashboard") + "#tab-books")


@bp.route("/books/<int:row_id>/delete", methods=["POST"])
@login_required
def delete_book(row_id):
    from app import get_store
    get_store().delete_book(row_id)
    return redirect(url_for("admin.dashboard") + "#tab-books")


# --- Song actions ---

@bp.route("/songs/<int:row_id>/toggle", methods=["POST"])
@login_required
def toggle_song(row_id):
    from app import get_store
    get_store().toggle_song_visible(row_id)
    return redirect(url_for("admin.dashboard") + "#tab-songs")


@bp.route("/songs/<int:row_id>/delete", methods=["POST"])
@login_required
def delete_song(row_id):
    from app import get_store
    get_store().delete_song(row_id)
    return redirect(url_for("admin.dashboard") + "#tab-songs")


# --- Message actions ---

@bp.route("/messages/<int:row_id>/delete", methods=["POST"])
@login_required
def delete_message(row_id):
    from app import get_store
    get_store().delete_contact_message(row_id)
    return redirect(url_for("admin.dashboard") + "#tab-messages")


# --- Data file editor ---

@bp.route("/data/<filename>", methods=["POST"])
@login_required
def save_data(filename):
    if filename not in EDITABLE_FILES:
        return "Not found", 404

    content = request.form.get("content", "").strip()
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as exc:
        from app import get_store
        ctx = _dashboard_ctx(
            get_store(),
            json_error=f"Invalid JSON in {filename}: {exc}",
            active_file=filename,
        )
        ctx["files"][filename] = content  # preserve what the user typed
        return render_template("admin/dashboard.html", **ctx), 400

    try:
        (DATA / filename).write_text(json.dumps(parsed, indent=2))
    except OSError as exc:
        from app import get_store
        ctx = _dashboard_ctx(
            get_store(),
            json_error=f"Could not write {filename}: {exc} (filesystem may be read-only)",
            active_file=filename,
        )
        ctx["files"][filename] = content
        return render_template("admin/dashboard.html", **ctx), 500

    return redirect(url_for("admin.dashboard") + "#tab-data")
