import random
from functools import wraps

from flask import Blueprint, render_template, jsonify

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
    response = random.choice(["Yes", "No"])
    return jsonify({"answer": response})
