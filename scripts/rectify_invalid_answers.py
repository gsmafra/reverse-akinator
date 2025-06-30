from tqdm import tqdm

from app.db_access import init_firebase
from app.db_access.rectification_queue import add_to_rectification_queue

VALID_ANSWERS = {"yes", "no", "ambiguous"}


def rectify_invalid_answers():
    db = init_firebase()
    canonical_ref = db.collection("canonical_answers")
    # Get all canonical answers
    docs = canonical_ref.get()
    invalid_docs = [doc for doc in docs if doc.to_dict().get("answer") not in VALID_ANSWERS]
    print(f"Found {len(invalid_docs)} docs with invalid answers.")
    for doc in tqdm(invalid_docs, desc="Adding to rectification queue"):
        data = doc.to_dict()
        character = data.get("character")
        question = data.get("question")
        answer = data.get("answer")
        add_to_rectification_queue(db, character, question, answer)


if __name__ == "__main__":
    rectify_invalid_answers()
