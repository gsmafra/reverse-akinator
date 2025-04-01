import random
from functools import wraps

from flask import Blueprint, render_template, jsonify, request

from .db_access import cache_answer, get_cached_answer
from .gemini import get_gemini_answer

blueprint = Blueprint('main', __name__)


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

current_character = None


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


@blueprint.route('/reset', methods=['GET'])
def reset_character():
    global current_character
    current_character = random.choice(CHARACTERS)
    print(f"New character selected: {current_character}")  # For debugging
    return jsonify({"message": "Character has been reset."})


@blueprint.route('/yes_or_no', methods=['GET'])
def yes_or_no():
    question = request.args.get('question')
    if question is None:
        return jsonify({"error": "Missing required parameter 'question'"}), 400
    prompt = f"Answer the following question in yes or no format about {current_character}: {question}"

    cached_answer = get_cached_answer(current_character, question)
    if cached_answer is not None:
        print(cached_answer)
        return jsonify({"answer": cached_answer})

    answer = get_gemini_answer(prompt)
    cache_answer(current_character, question, answer)
    key = "answer" if isinstance(answer, bool) else "error"
    print(answer)
    return jsonify({key: answer})
