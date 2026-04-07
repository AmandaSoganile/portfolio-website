from flask import Blueprint, jsonify, request
from app import load_json, get_store

bp = Blueprint("fun_facts", __name__)

ALLOWED_EMOJIS = {"😂", "💀", "😭", "🫶", "👀"}


def _facts_with_reactions():
    facts = load_json("fun_facts.json")
    store = get_store()
    for fact in facts:
        fact["reactions"] = store.get_reactions(fact["id"])
    return facts


@bp.route("/fun-fact")
def fun_fact_random():
    import random
    facts = _facts_with_reactions()
    return jsonify(random.choice(facts)) if facts else ("", 404)


@bp.route("/fun-fact/all")
def fun_facts_all():
    return jsonify(_facts_with_reactions())


@bp.route("/fun-fact/<int:fact_id>/reactions")
def get_reactions(fact_id):
    facts = load_json("fun_facts.json")
    valid_ids = {f["id"] for f in facts}
    if fact_id not in valid_ids:
        return jsonify({"status": "error", "message": "fact not found"}), 404
    return jsonify({
        "fact_id": fact_id,
        "reactions": get_store().get_reactions(fact_id),
    })


@bp.route("/fun-fact/<int:fact_id>/react", methods=["POST"])
def add_reaction(fact_id):
    facts = load_json("fun_facts.json")
    valid_ids = {f["id"] for f in facts}
    if fact_id not in valid_ids:
        return jsonify({"status": "error", "message": "fact not found"}), 404

    body = request.get_json(silent=True) or {}
    emoji = body.get("emoji", "").strip()
    if not emoji or emoji not in ALLOWED_EMOJIS:
        return jsonify({
            "status": "error",
            "message": f"emoji must be one of: {', '.join(sorted(ALLOWED_EMOJIS))}"
        }), 400

    reactions = get_store().add_reaction(fact_id, emoji)
    return jsonify({"status": "ok", "reactions": reactions})
