import random
from functools import wraps

from flask import Blueprint, render_template, jsonify, request

from app.db_access import cache_answer, get_cached_answer
from app.gemini import get_gemini_answer

blueprint = Blueprint("main", __name__)


CHARACTERS = [
    "Pikachu",
    "Mario",
    "Harry Potter",
    "Wonder Woman",
    "Spider-Man",
    "Mickey Mouse",
    "Luke Skywalker",
    "Hermione Granger",
    "Batman",
    "SpongeBob SquarePants",
]

CURRENT_CHARACTER = None


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
    # to-do: persist character in db
    # pylint: disable=W0603
    global CURRENT_CHARACTER
    CURRENT_CHARACTER = random.choice(CHARACTERS)
    print(f"New character selected: {CURRENT_CHARACTER}")  # For debugging
    return jsonify({"message": "Character has been reset."})


@blueprint.route("/yes_or_no", methods=["GET"])
def yes_or_no():
    question = request.args.get("question")
    if question is None:
        return jsonify({"error": "Missing required parameter 'question'"}), 400
    prompt = f"Answer the following question in yes or no format about {CURRENT_CHARACTER}: {question}"

    cached_answer = get_cached_answer(CURRENT_CHARACTER, question)
    if cached_answer is not None:
        print(cached_answer)
        return jsonify({"answer": cached_answer})

    answer = get_gemini_answer(prompt)
    cache_answer(CURRENT_CHARACTER, question, answer)
    key = "answer" if isinstance(answer, bool) else "error"
    print(answer)
    return jsonify({key: answer})
