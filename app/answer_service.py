from app.db_access import (
    get_character,
    get_canonical_answer,
    set_canonical_answer,
    update_session,
    add_thumbs_down,
    get_thumbs_down_answers,
    update_answer,
)
from app.gemini import get_gemini_answer
from app.utils import normalize_question


def get_or_generate_answer(db, device_id, question):
    question = normalize_question(question)
    current_character = get_character(db, device_id)

    answer = get_canonical_answer(db, current_character, question)
    if answer is None:
        answer = get_gemini_answer(current_character, question)
        set_canonical_answer(db, current_character, question, answer)

    session_answers = update_session(db, device_id, question, answer)
    key = "answer" if answer in ["yes", "no", "ambiguous"] else "error"
    return {key: answer, "session_answers": session_answers}


def thumbs_down_answer(db, question, character, answer):
    add_thumbs_down(db, question, character, answer)


def get_answers_to_rectify(db):
    return get_thumbs_down_answers(db)


def rectify_answer_service(db, character, question, rectified_answer):
    update_answer(db, character, question, rectified_answer, thumbs_down=False)
