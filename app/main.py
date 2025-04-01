import random
from functools import wraps

from flask import Blueprint, render_template, jsonify

blueprint = Blueprint('main', __name__)


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


@blueprint.route('/yes_or_no', methods=['GET'])
def yes_or_no():
    response = random.choice(["Yes", "No"])
    return jsonify({"answer": response})
