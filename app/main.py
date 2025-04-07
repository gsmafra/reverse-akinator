import random
from functools import wraps

from flask import Blueprint, render_template, jsonify, request

from app.resources.resources import CHARACTERS, CHARACTER_IMAGE_URLS
from app.db_access import (
    add_thumbs_down,
    cache_answer,
    get_cached_answer,
    get_character,
    set_character,
    update_session_answer,
)
from app.gemini import get_gemini_answer

blueprint = Blueprint("main", __name__)


def handle_exceptions(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        # pylint: disable=W0718
        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 500

    return wrapper


@blueprint.route("/")
def index():
    return render_template("index.html")


@blueprint.route("/reset", methods=["GET"])
def reset_character():
    current_character = random.choice(CHARACTERS)
    print(f"New character selected: {current_character}")  # For debugging
    device_id = request.remote_addr
    set_character(device_id, current_character)
    return jsonify({"message": "Character has been reset."})


@blueprint.route("/ask", methods=["GET"])
def ask():
    question = request.args.get("question")
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


@blueprint.route("/reveal", methods=["GET"])
def reveal_character():
    current_character = get_character(request.remote_addr)
    return jsonify(
        {
            "character": current_character,
            "image_url": CHARACTER_IMAGE_URLS[current_character],
        }
    )


@blueprint.route("/thumbs_down", methods=["POST"])
def thumbs_down():
    data = request.get_json()
    question = data["question"]
    character = data["character"]
    answer = data["answer"]

    # Call the DB function to add a thumbs down flag
    add_thumbs_down(question, character, answer)

    return jsonify({"message": "Thumbs down added successfully"})


@blueprint.route('/rectify')
def rectify():
    return render_template('rectify.html')
