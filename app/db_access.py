import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import ArrayUnion
from google.cloud.firestore import FieldFilter

from app.config import config


def init_firebase():
    firebase_key_path = config.FIREBASE_KEY_PATH
    firebase_cred = credentials.Certificate(firebase_key_path)
    firebase_admin.initialize_app(firebase_cred)
    return firestore.client()


def cache_answer(db, character, question, answer):
    doc_ref = db.collection("answers").document()
    doc_ref.set({"character": character, "question": question, "answer": answer})


def get_cached_answer(db, character, question):
    answers_ref = db.collection("answers")
    query = answers_ref.where(filter=FieldFilter("character", "==", character)).where(
        filter=FieldFilter("question", "==", question)
    )
    results = query.get()
    if not len(results) > 0:
        return None

    answer = results[0].to_dict()["answer"]
    if isinstance(answer, bool):
        answer = "yes" if answer else "no"

    return answer


def get_character(db, device_id):
    doc_ref = db.collection("devices").document(device_id)
    doc = doc_ref.get()
    return doc.to_dict()["character"]


def set_character(db, device_id, character):
    doc_ref = db.collection("devices").document(device_id)
    doc_ref.set({"character": character})


def update_session_answer(db, device_id, question, answer):
    """
    Appends a new question/answer pair to the 'session_answers' array field.

    Note: While 'session_answers' is modeled as an array, it does not grow indefinitely.
    At the start of each new session, we call 'set_character', which overwrites the 
    entire document and resets any previous session data, including 'session_answers'.
    """
    doc_ref = db.collection("devices").document(device_id)
    doc_ref.update(
        {"session_answers": ArrayUnion([{"question": question, "answer": answer}])}
    )
    updated_doc = doc_ref.get().to_dict()
    return updated_doc.get("session_answers", [])


def add_thumbs_down(db, question, character, answer):
    answers_ref = db.collection("answers")
    query = (
        answers_ref.select(field_paths=["question", "character", "answer"])
        .where(filter=FieldFilter("question", "==", question))
        .where(filter=FieldFilter("character", "==", character))
        .where(filter=FieldFilter("answer", "==", answer))
    )
    results = query.get()
    for doc in results:
        doc.reference.set({"thumbs_down": True}, merge=True)


def get_thumbs_down_answers(db):
    answers_ref = db.collection("answers")
    query = answers_ref.where(filter=FieldFilter("thumbs_down", "==", True))
    results = query.get()
    return [doc.to_dict() for doc in results]


def update_answer(db, character, question, answer, thumbs_down):
    answers_ref = db.collection("answers")
    query = answers_ref.where(filter=FieldFilter("character", "==", character)).where(
        filter=FieldFilter("question", "==", question)
    )
    results = query.get()
    for doc in results:
        doc.reference.update(
            {
                "answer": answer,
                "thumbs_down": thumbs_down,
            }
        )
