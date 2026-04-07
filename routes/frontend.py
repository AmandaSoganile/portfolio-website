from flask import Blueprint, render_template

bp = Blueprint("frontend", __name__)


@bp.route("/")
def landing():
    return render_template("landing.html")


@bp.route("/about")
def about_page():
    return render_template("about.html")


@bp.route("/journey")
def journey_page():
    return render_template("journey.html")


@bp.route("/fun-facts")
def fun_facts_page():
    return render_template("fun_facts.html")


@bp.route("/projects")
def projects_page():
    return render_template("projects.html")


@bp.route("/books")
def books_page():
    return render_template("books.html")


@bp.route("/songs")
def songs_page():
    return render_template("songs.html")


@bp.route("/play")
def game_page():
    return render_template("game.html")


@bp.route("/contact")
def contact_page():
    return render_template("contact.html")
