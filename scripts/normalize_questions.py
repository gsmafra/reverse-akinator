import firebase_admin
from firebase_admin import credentials, firestore

from app.config import config
from app.utils import normalize_question


def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(config.FIREBASE_KEY_PATH)
        firebase_admin.initialize_app(cred)
    return firestore.client()


def main():
    db = initialize_firebase()
    results = db.collection("answers").get()
    for doc in results:
        question = doc.to_dict()["question"]
        normalized_question = normalize_question(question)
        if question != normalized_question:
            print(f"Updating question: {question} -> {normalized_question}")
            doc.reference.update({"question": normalize_question(question)})


if __name__ == "__main__":
    main()
