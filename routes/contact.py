import os
from flask import Blueprint, jsonify, request, current_app

bp = Blueprint("contact", __name__)


def _send_via_ses(to: str, name: str, sender_email: str, message: str) -> None:
    import boto3
    client = boto3.client("ses", region_name="us-east-1")
    client.send_email(
        Source=to,
        Destination={"ToAddresses": [to]},
        Message={
            "Subject": {"Data": f"Portfolio message from {name}"},
            "Body": {
                "Text": {
                    "Data": (
                        f"Name: {name}\n"
                        f"Email: {sender_email}\n\n"
                        f"{message}"
                    )
                }
            },
        },
    )


def _send_notification(name: str, slack_email: str, message: str) -> None:
    contact_email = current_app.config.get("CONTACT_EMAIL", "")
    print(
        f"[contact] new message\n"
        f"  from: {name} ({slack_email})\n"
        f"  message: {message}"
    )
    if not contact_email:
        return
    try:
        _send_via_ses(contact_email, name, slack_email, message)
        print(f"[contact] email sent to {contact_email}")
    except Exception as exc:
        print(f"[contact] SES send failed: {exc}")


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
