from flask import Blueprint, jsonify, request
from app import load_json, get_store

bp = Blueprint("songs", __name__)


@bp.route("/songs")
def get_songs():
    return jsonify({
        "mine": load_json("songs_mine.json"),
        "community": get_store().get_song_submissions(),  # visible-only
    })


@bp.route("/songs", methods=["POST"])
def add_song():
    body = request.get_json(silent=True) or {}
    name = (body.get("name") or "").strip()
    title = (body.get("title") or "").strip()
    artist = (body.get("artist") or "").strip()
    note = (body.get("note") or "").strip()

    if not name or not title:
        return jsonify({"status": "error", "message": "name and title are required"}), 400

    get_store().add_song(name, title, artist, note)
    return jsonify({"status": "ok", "message": "Song added!"})
