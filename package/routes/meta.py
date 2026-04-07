import os
from datetime import datetime, timezone
from flask import Blueprint, jsonify
from app import git_sha, version

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
