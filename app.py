import json
import os
import random
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, request, render_template, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE = Path(__file__).parent
DATA = BASE / "data"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load(filename):
    with open(DATA / filename) as f:
        return json.load(f)


def git_sha():
    """Return the current git commit SHA, or 'unknown' if not in a git repo."""
    sha = os.environ.get("GIT_SHA")
    if sha:
        return sha
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, cwd=BASE
        )
        return result.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def version():
    try:
        return (BASE / "VERSION").read_text().strip()
    except FileNotFoundError:
        return "0.0.0"


# ---------------------------------------------------------------------------
# Routes — API
# ---------------------------------------------------------------------------

@app.route("/meta")
def meta():
    return jsonify({
        "version": version(),
        "deployed_at": os.environ.get("DEPLOY_TIMESTAMP", datetime.now(timezone.utc).isoformat()),
        "commit_sha": git_sha(),
        "environment": os.environ.get("FLASK_ENV", "development"),
    })


@app.route("/about")
def about():
    return jsonify(load("about.json"))


@app.route("/projects")
def projects():
    return jsonify(load("projects.json"))


@app.route("/fun-fact")
def fun_fact():
    facts = load("fun_facts.json")
    return jsonify(random.choice(facts))


@app.route("/fun-fact/all")
def fun_facts_all():
    return jsonify(load("fun_facts.json"))


@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not email or not message:
        return jsonify({"status": "error", "message": "name, email, and message are required"}), 400

    # TODO: wire up to Slack webhook or email when deploying to AWS
    print(f"[contact] from={email} name={name} message={message!r}")

    return jsonify({"status": "ok", "message": "Thanks! I'll get back to you soon."})


# ---------------------------------------------------------------------------
# Route — Frontend
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)
