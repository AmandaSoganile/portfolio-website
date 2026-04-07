from flask import Blueprint, jsonify, request
from app import load_json, get_store

bp = Blueprint("books", __name__)


@bp.route("/books")
def get_books():
    return jsonify({
        "mine": load_json("books_mine.json"),
        "community": get_store().get_book_submissions(),
    })


@bp.route("/books", methods=["POST"])
def add_book():
    body = request.get_json(silent=True) or {}
    name = (body.get("name") or "").strip()
    title = (body.get("title") or "").strip()
    author = (body.get("author") or "").strip()

    if not name or not title:
        return jsonify({"status": "error", "message": "name and title are required"}), 400

    get_store().add_book(name, title, author)
    return jsonify({"status": "ok", "message": "Book added!"})
