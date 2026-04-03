from flask import Blueprint, jsonify
from app import load_json

bp = Blueprint("about", __name__)


@bp.route("/about")
def about():
    return jsonify(load_json("about.json"))


@bp.route("/projects")
def projects():
    return jsonify(load_json("projects.json"))
