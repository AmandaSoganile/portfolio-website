from flask import Blueprint, jsonify, request, current_app

bp = Blueprint("contact", __name__)


def _send_notification(name: str, slack_email: str, message: str) -> None:
    contact_email = current_app.config.get("CONTACT_EMAIL", "")
    if contact_email:
        # TODO Phase 2: send via AWS SES
        print(f"[contact] would email {contact_email}")
    print(
        f"[contact] new message\n"
        f"  from: {name} ({slack_email})\n"
        f"  message: {message}"
    )


@bp.route("/contact", methods=["POST"])
def contact():
    body = request.get_json(silent=True) or {}
    name = (body.get("name") or "").strip()
    slack_email = (body.get("slack_email") or "").strip()
    message = (body.get("message") or "").strip()

    if not name or not slack_email or not message:
        return jsonify({
            "status": "error",
            "message": "name, slack_email, and message are required"
        }), 400

    _send_notification(name, slack_email, message)
    return jsonify({"status": "ok", "message": "Thanks! I'll get back to you soon."})
