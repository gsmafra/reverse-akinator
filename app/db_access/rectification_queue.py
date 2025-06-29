from google.cloud.firestore import FieldFilter, SERVER_TIMESTAMP


def add_to_rectification_queue(db, character, question, answer):
    """
    Add a question/answer pair to the rectification queue.
    This is useful for tracking answers that need to be reviewed or corrected.
    """
    doc_ref = db.collection("rectification_queue").document()
    doc_ref.set({"character": character, "question": question, "answer": answer, "timestamp": SERVER_TIMESTAMP})


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
