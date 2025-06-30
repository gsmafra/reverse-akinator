from google.cloud.firestore import FieldFilter
from tqdm import tqdm

from app.db_access import init_firebase


def convert_boolean_answers():
    db = init_firebase()
    canonical_ref = db.collection("canonical_answers")
    query = canonical_ref.where(filter=FieldFilter("answer", "in", [True, False]))
    docs = query.get()
    print(f"Found {len(docs)} docs with boolean answers.")
    for doc in tqdm(docs, desc="Converting boolean answers"):
        answer = doc.to_dict().get("answer")
        if answer is True:
            new_answer = "yes"
        elif answer is False:
            new_answer = "no"
        else:
            continue
        doc.reference.update({"answer": new_answer})


if __name__ == "__main__":
    convert_boolean_answers()
