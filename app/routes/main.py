from flask import Blueprint, current_app, render_template, jsonify, request

from app.services.answer import get_or_generate_answer, thumbs_down_answer
from app.services.character import (
    start_themed_game_service,
    start_regular_game_service,
    reveal_character_service,
)

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/select-theme")
def select_theme():
    return render_template("select-theme.html")


@main_bp.route("/themed/<category>")
def themed_category(category):
    # Pass the category to the template for JS to pick up
    return render_template("themed.html", category=category)


@main_bp.route("/reset", methods=["POST"])
def start_regular_game():
    db = current_app.db
    data = request.get_json()
    device_id = data.get("device_id")
    result = start_regular_game_service(db, device_id)
    if "error" in result:
        return jsonify({"error": result["error"]}), 400
    return jsonify(result)


@main_bp.route("/ask", methods=["GET"])
def ask():
    db = current_app.db
    question = request.args.get("question")
    device_id = request.args.get("device_id")
    return jsonify(get_or_generate_answer(db, device_id, question))


@main_bp.route("/reveal", methods=["GET"])
def reveal_character():
    db = current_app.db
    device_id = request.args.get("device_id")
    result = reveal_character_service(db, device_id)
    if "error" in result:
        return jsonify({"error": result["error"]}), 400
    return jsonify(result)


@main_bp.route("/thumbs_down", methods=["POST"])
def thumbs_down():
    db = current_app.db
    data = request.get_json()
    question = data["question"]
    character = data["character"]
    answer = data["answer"]
    device_id = data["device_id"]

    thumbs_down_answer(db, question, character, answer, device_id)
    return jsonify({"message": "Thumbs down added successfully"})


@main_bp.route("/start-themed-game", methods=["POST"])
def start_themed_game():
    db = current_app.db
    data = request.get_json()
    category = data.get("category")
    device_id = data.get("device_id")

    result = start_themed_game_service(db, device_id, category)
    if "error" in result:
        return jsonify({"error": result["error"]}), 400
    return jsonify(result)
