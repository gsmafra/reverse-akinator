from google.cloud.firestore import SERVER_TIMESTAMP
from google.cloud.firestore import FieldFilter


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


def set_canonical_answer(db, character, question, answer):
    doc_ref = db.collection("canonical_answers").document()
    doc_ref.set({"character": character, "question": question, "answer": answer, "timestamp": SERVER_TIMESTAMP})


def update_canonical_answer(db, character, question, answer):
    answers_ref = db.collection("canonical_answers")
    query = answers_ref.where(filter=FieldFilter("character", "==", character)).where(
        filter=FieldFilter("question", "==", question)
    )
    results = query.get()
    for doc in results:
        doc.reference.update({"answer": answer})
