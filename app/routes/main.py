import random

from flask import Blueprint, current_app, render_template, jsonify, request

from app.resources.resources import CHARACTERS, CHARACTER_IMAGE_URLS
from app.db_access.devices import get_character, set_character
from app.services.answer import get_or_generate_answer, thumbs_down_answer

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/reset", methods=["POST"])
def reset_character():
    db = current_app.db
    data = request.get_json()
    device_id = data.get("device_id")
    current_character = random.choice(CHARACTERS)
    print(f"New character selected for device {device_id}: {current_character}")
    set_character(db, device_id, current_character)
    return jsonify({"message": "Character has been reset."})


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
    current_character = get_character(db, device_id)
    return jsonify(
        {
            "character": current_character,
            "image_url": CHARACTER_IMAGE_URLS[current_character],
        }
    )


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
