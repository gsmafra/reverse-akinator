from google.cloud.firestore import SERVER_TIMESTAMP
from google.cloud.firestore_v1 import ArrayUnion


def get_character(db, device_id):
    doc_ref = db.collection("devices").document(device_id)
    doc = doc_ref.get()
    return doc.to_dict()["character"]


def set_character(db, device_id, character):
    doc_ref = db.collection("devices").document(device_id)
    doc_ref.set({"character": character, "timestamp": SERVER_TIMESTAMP}, merge=True)


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
