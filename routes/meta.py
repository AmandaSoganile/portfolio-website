import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from flask import Blueprint, jsonify

_BASE = Path(__file__).parent.parent


def git_sha():
    sha = os.environ.get("GIT_SHA")
    if sha:
        return sha
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, cwd=_BASE
        )
        return result.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def version():
    try:
        return (_BASE / "VERSION").read_text().strip()
    except FileNotFoundError:
        return "0.0.0"

bp = Blueprint("meta", __name__)


@bp.route("/meta")
def meta():
    return jsonify({
        "version": version(),
        "deployed_at": os.environ.get(
            "DEPLOY_TIMESTAMP",
            datetime.now(timezone.utc).isoformat()
        ),
        "commit_sha": git_sha(),
        "environment": os.environ.get("FLASK_ENV", "development"),
    })
