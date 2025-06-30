from app.db_access.canonical_answers import get_canonical_answer, set_canonical_answer, update_canonical_answer
from app.db_access.devices import get_character, update_session
from app.db_access.served_answers import add_thumbs_down, set_served_answer
from app.db_access.rectification_queue import (
    add_to_rectification_queue,
    get_rectification_queue,
    remove_from_rectification_queue,
)
from app.llm.gemini import get_gemini_answer
from app.utils import normalize_question


def get_or_generate_answer(db, device_id, question):
    question = normalize_question(question)
    current_character = get_character(db, device_id)

    answer = get_canonical_answer(db, current_character, question)
    if answer is None:
        answer, pipeline_name = get_gemini_answer(current_character, question)
        if answer in ["yes", "no", "ambiguous"]:
            set_canonical_answer(db, current_character, question, answer)
            set_served_answer(db, current_character, question, answer, pipeline_name, device_id)

    session_answers = update_session(db, device_id, question, answer)
    key = "answer" if answer in ["yes", "no", "ambiguous"] else "error"
    return {key: answer, "session_answers": session_answers}


def thumbs_down_answer(db, question, character, answer, device_id):
    add_thumbs_down(db, question, character, answer, device_id)
    add_to_rectification_queue(db, character, question, answer)


def get_answers_to_rectify(db):
    return get_rectification_queue(db)


def rectify_answer_service(db, character, question, original_answer, rectified_answer):
    update_canonical_answer(db, character, question, rectified_answer)
    remove_from_rectification_queue(db, character, question, original_answer)
