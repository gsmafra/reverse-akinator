from flask import Blueprint, render_template, jsonify, request, current_app

from app.db_access import get_thumbs_down_answers, update_answer

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/ping")
def ping():
    return jsonify({"message": "pong"})


@admin_bp.route("/rectify")
def rectify():
    return render_template("rectify.html")


@admin_bp.route("/answers_to_rectify")
def answers_to_rectify():
    db = current_app.db
    return jsonify(get_thumbs_down_answers(db))


@admin_bp.route("/rectify_answer", methods=["POST"])
def rectify_answer():
    db = current_app.db
    data = request.get_json()
    character = data["character"]
    question = data["question"]
    answer = data["rectified_answer"]
    update_answer(db, character, question, answer, thumbs_down=False)
    return jsonify({"message": "Answer rectified successfully"})
