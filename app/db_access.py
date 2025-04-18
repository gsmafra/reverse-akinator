import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import FieldFilter

from app.config import config


def init_firebase():
    firebase_key_path = config.FIREBASE_KEY_PATH
    firebase_cred = credentials.Certificate(firebase_key_path)
    firebase_admin.initialize_app(firebase_cred)
    return firestore.client()


db = init_firebase()


def cache_answer(character, question, answer):
    doc_ref = db.collection("answers").document()
    doc_ref.set({"character": character, "question": question, "answer": answer})


def get_cached_answer(character, question):
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


def get_character(device_id):
    doc_ref = db.collection("devices").document(device_id)
    doc = doc_ref.get()
    return doc.to_dict()["character"]


def set_character(device_id, character):
    doc_ref = db.collection("devices").document(device_id)
    doc_ref.set({"character": character})


def update_session_answer(device_id, question, answer):
    doc_ref = db.collection("devices").document(device_id)
    doc_data = doc_ref.get().to_dict()
    if "session_answers" not in doc_data:
        doc_data["session_answers"] = []
    doc_data["session_answers"].append({"question": question, "answer": answer})
    doc_ref.set(doc_data)
    return doc_data["session_answers"]


def add_thumbs_down(question, character, answer):
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


def get_thumbs_down_answers():
    answers_ref = db.collection("answers")
    query = answers_ref.where(filter=FieldFilter("thumbs_down", "==", True))
    results = query.get()
    return [doc.to_dict() for doc in results]


def update_answer(character, question, answer, thumbs_down):
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
