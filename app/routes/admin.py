from flask import Blueprint, render_template, jsonify, request, current_app

from app.services.answer import get_answers_to_rectify, rectify_answer_service
from app.services.analytics import get_monolithic_analytics, get_logistic_analytics

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/ping")
def ping():
    return jsonify({"message": "pong"})


@admin_bp.route("/analytics/monolithic")
def analytics_monolithic():
    return render_template("analytics/monolithic.html")


@admin_bp.route("/analytics/logistic")
def analytics_logistic():
    return render_template("analytics/logistic.html")


@admin_bp.route("/rectify")
def rectify():
    return render_template("rectify.html")


@admin_bp.route("/answers_to_rectify")
def answers_to_rectify():
    db = current_app.db
    return jsonify(get_answers_to_rectify(db))


@admin_bp.route("/rectify_answer", methods=["POST"])
def rectify_answer():
    db = current_app.db
    data = request.get_json()
    character = data["character"]
    question = data["question"]
    original_answer = data["original_answer"]
    rectified_answer = data["rectified_answer"]
    rectify_answer_service(db, character, question, original_answer, rectified_answer)
    return jsonify({"message": "Answer rectified successfully"})


@admin_bp.route("/monolithic_analytics_data")
def monolithic_analytics_data():
    db = current_app.db
    monolithic_analytics = get_monolithic_analytics(db)
    return jsonify(monolithic_analytics)


@admin_bp.route("/logistic_analytics_data")
def logistic_analytics_data():
    db = current_app.db
    logistic_analytics = get_logistic_analytics(db)
    return jsonify(logistic_analytics)
