from google.cloud.firestore import FieldFilter, SERVER_TIMESTAMP


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
            "timestamp": SERVER_TIMESTAMP,
        }
    )


def get_all_served_answers(db):
    """
    Fetch all documents from the served_answers collection.
    """
    served_answers_ref = db.collection("served_answers")
    return [doc.to_dict() for doc in served_answers_ref.stream()]
