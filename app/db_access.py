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


def add_to_rectification_queue(db, character, question, answer):
    """
    Add a question/answer pair to the rectification queue.
    This is useful for tracking answers that need to be reviewed or corrected.
    """
    doc_ref = db.collection("rectification_queue").document()
    doc_ref.set({"character": character, "question": question, "answer": answer})


def get_rectification_queue(db):
    """
    Retrieve all entries in the rectification queue.
    This is useful for reviewing answers that need rectification.
    """
    queue_ref = db.collection("rectification_queue")
    results = queue_ref.get()
    return [doc.to_dict() for doc in results]


def remove_from_rectification_queue(db, character, question, answer):
    """
    Remove a specific question/answer pair from the rectification queue.
    This is useful after an answer has been reviewed and rectified.
    """
    queue_ref = db.collection("rectification_queue")
    query = (
        queue_ref.where(filter=FieldFilter("character", "==", character))
        .where(filter=FieldFilter("question", "==", question))
        .where(filter=FieldFilter("answer", "==", answer))
    )
    results = query.get()
    for doc in results:
        doc.reference.delete()


def set_canonical_answer(db, character, question, answer):
    doc_ref = db.collection("canonical_answers").document()
    doc_ref.set({"character": character, "question": question, "answer": answer})


def set_served_answer(db, character, question, answer, pipeline_name, device_id):
    """
    Store the answer served by the model along with its pipeline ID.
    This is useful for tracking which model version provided the answer.
    """
    doc_ref = db.collection("served_answers").document()
    doc_ref.set(
        {
            "character": character,
            "question": question,
            "answer": answer,
            "pipeline_name": pipeline_name,
            "device_id": device_id,
        }
    )


def get_canonical_answer(db, character, question):
    answers_ref = db.collection("canonical_answers")
    query = answers_ref.where(filter=FieldFilter("character", "==", character)).where(
        filter=FieldFilter("question", "==", question)
    )
    results = query.get()
    if not len(results) > 0:
        return None

    # we shouldn't have more than one canonical answer for a character/question pair
    answer = results[0].to_dict()["answer"]

    # old answers were stored as booleans when we didn't have "ambiguous"
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


def update_session(db, device_id, question, answer):
    """
    Appends a new question/answer pair to the 'session_answers' array field.

    Note: While 'session_answers' is modeled as an array, it does not grow indefinitely.
    At the start of each new session, we call 'set_character', which overwrites the
    entire document and resets any previous session data, including 'session_answers'.
    """
    doc_ref = db.collection("devices").document(device_id)
    doc_ref.update({"session_answers": ArrayUnion([{"question": question, "answer": answer}])})
    updated_doc = doc_ref.get().to_dict()
    return updated_doc.get("session_answers", [])


def add_thumbs_down(db, question, character, answer, device_id):
    answers_ref = db.collection("served_answers")
    query = (
        answers_ref.select(field_paths=["question", "character", "answer", "device_id"])
        .where(filter=FieldFilter("question", "==", question))
        .where(filter=FieldFilter("character", "==", character))
        .where(filter=FieldFilter("answer", "==", answer))
        .where(filter=FieldFilter("device_id", "==", device_id))
    )
    results = query.get()
    for doc in results:
        doc.reference.set({"thumbs_down": True, "rectified": False}, merge=True)


def get_thumbs_down_answers(db):
    answers_ref = db.collection("served_answers")
    query = answers_ref.where(filter=FieldFilter("thumbs_down", "==", True)).where(
        filter=FieldFilter("rectified", "==", False)
    )
    results = query.get()
    return [doc.to_dict() for doc in results]


def update_canonical_answer(db, character, question, answer):
    answers_ref = db.collection("canonical_answers")
    query = answers_ref.where(filter=FieldFilter("character", "==", character)).where(
        filter=FieldFilter("question", "==", question)
    )
    results = query.get()
    for doc in results:
        doc.reference.update({"answer": answer})


def rectify_served_answer(db, character, question, original_answer):
    answers_ref = db.collection("served_answers")
    query = (
        answers_ref.where(filter=FieldFilter("character", "==", character))
        .where(filter=FieldFilter("question", "==", question))
        .where(filter=FieldFilter("answer", "==", original_answer))
    )
    results = query.get()
    for doc in results:
        doc.reference.update({"rectified": True})
