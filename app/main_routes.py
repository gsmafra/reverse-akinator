import random

from flask import Blueprint, render_template, jsonify, request

from app.resources.resources import CHARACTERS, CHARACTER_IMAGE_URLS
from app.db_access import (
    get_character,
    set_character,
    get_cached_answer,
    cache_answer,
    update_session_answer,
    add_thumbs_down,
)
from app.gemini import get_gemini_answer

main_bp = Blueprint("main", __name__)


def normalize_question(question):
    question = question.strip()
    question = question[0].upper() + question[1:]
    while question.endswith("?"):
        question = question[:-1]
    return question


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/reset", methods=["GET"])
def reset_character():
    current_character = random.choice(CHARACTERS)
    print(f"New character selected: {current_character}")  # For debugging
    device_id = request.remote_addr
    set_character(device_id, current_character)
    return jsonify({"message": "Character has been reset."})


@main_bp.route("/ask", methods=["GET"])
def ask():
    question = request.args.get("question")
    question = normalize_question(question)
    if question is None:
        return jsonify({"error": "Missing required parameter 'question'"}), 400
    device_id = request.remote_addr
    current_character = get_character(device_id)

    answer = get_cached_answer(current_character, question)
    if answer is None:
        answer = get_gemini_answer(current_character, question)
        cache_answer(current_character, question, answer)

    session_answers = update_session_answer(device_id, question, answer)
    key = "answer" if answer in ["yes", "no", "ambiguous"] else "error"
    return jsonify({key: answer, "session_answers": session_answers})


@main_bp.route("/reveal", methods=["GET"])
def reveal_character():
    current_character = get_character(request.remote_addr)
    return jsonify(
        {
            "character": current_character,
            "image_url": CHARACTER_IMAGE_URLS[current_character],
        }
    )


@main_bp.route("/thumbs_down", methods=["POST"])
def thumbs_down():
    data = request.get_json()
    question = data["question"]
    character = data["character"]
    answer = data["answer"]

    add_thumbs_down(question, character, answer)

    return jsonify({"message": "Thumbs down added successfully"})
