import os
import random
from functools import wraps

import google.generativeai as genai
from flask import Blueprint, render_template, jsonify, request

blueprint = Blueprint('main', __name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

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


def _parse_gemini_response(response):
    if not response.candidates:
        return "No response from the model"

    first_candidate = response.candidates[0]

    if not first_candidate.content:
        return "No content in the first candidate"
    if not first_candidate.content.parts:
        return "No content parts in the first candidate"

    first_part = first_candidate.content.parts[0]

    if not first_part.text:
        return "No text in the first part of the first candidate"

    answer = first_part.text.strip()  # Remove potential whitespace

    if answer.lower() not in ["yes", "no"]:
        return f"Invalid answer format: {answer}"

    return answer.lower()


@blueprint.route('/yes_or_no', methods=['GET'])
def yes_or_no():
    question = request.args.get('question')
    if question is None:
        return jsonify({"error": "Missing required parameter 'question'"}), 400
    prompt = f"Answer the following question in yes or no format about {current_character}: {question}"
    response = model.generate_content(
        contents=prompt,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=2,
            temperature=0,
            top_p=1,
            top_k=1,
        ),
        stream=False,
    )
    answer = _parse_gemini_response(response)
    key = "answer" if answer.lower() in ["yes", "no"] else "error"
    print(answer)
    return jsonify({key: answer})
