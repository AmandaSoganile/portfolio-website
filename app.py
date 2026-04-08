import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask
from flask_cors import CORS


BASE = Path(__file__).parent
DATA = BASE / "data"


def load_json(filename):
    with open(DATA / filename) as f:
        return json.load(f)


def git_sha():
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


def get_store():
    from flask import current_app, g
    from store import Store
    if "store" not in g:
        g.store = Store(current_app.config["DATABASE"])
    return g.store


def create_app(config=None):
    app = Flask(__name__)
    CORS(app)

    app.config["DATABASE"] = "/tmp/portfolio.db" if os.environ.get("AWS_LAMBDA_FUNCTION_NAME") else str(BASE / "portfolio.db")
    app.config["STORAGE_BACKEND"] = os.environ.get("STORAGE_BACKEND", "sqlite")
    app.config["CONTACT_EMAIL"] = os.environ.get("CONTACT_EMAIL", "soganileamanda@gmail.com")
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 31536000  # 1 year — cache-busted via ?v=N
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod")
    app.config["ADMIN_PASSWORD"] = os.environ.get("ADMIN_PASSWORD", "")
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    if config:
        app.config.update(config)

    from routes.meta import bp as meta_bp
    from routes.about import bp as about_bp
    from routes.fun_facts import bp as fun_facts_bp
    from routes.books import bp as books_bp
    from routes.songs import bp as songs_bp
    from routes.contact import bp as contact_bp
    from routes.admin import bp as admin_bp

    from routes.frontend import bp as frontend_bp

    app.register_blueprint(meta_bp,       url_prefix='/api')
    app.register_blueprint(about_bp,      url_prefix='/api')
    app.register_blueprint(fun_facts_bp,  url_prefix='/api')
    app.register_blueprint(books_bp,      url_prefix='/api')
    app.register_blueprint(songs_bp,      url_prefix='/api')
    app.register_blueprint(contact_bp,    url_prefix='/api')
    app.register_blueprint(admin_bp)
    app.register_blueprint(frontend_bp)

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
else:
    # Lambda handler — only initialized when imported by Lambda runtime
    try:
        from mangum import Mangum
        from asgiref.wsgi import WsgiToAsgi
        handler = Mangum(WsgiToAsgi(create_app()), lifespan="off")
    except ImportError:
        pass
