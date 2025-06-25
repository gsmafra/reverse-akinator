from app.db_access import init_firebase
from app.utils import normalize_question


def main():
    db = init_firebase()
    results = db.collection("answers").get()
    for doc in results:
        question = doc.to_dict()["question"]
        normalized_question = normalize_question(question)
        if question != normalized_question:
            print(f"Updating question: {question} -> {normalized_question}")
            doc.reference.update({"question": normalize_question(question)})


if __name__ == "__main__":
    main()
