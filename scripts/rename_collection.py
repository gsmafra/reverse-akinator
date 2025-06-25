from tqdm import tqdm

from app.db_access import init_firebase

BATCH_SIZE = 500


def main():
    old_collection_name = input("Enter the current name of the collection to rename: ")
    new_collection_name = input("Enter the new name of the collection: ")

    db = init_firebase()

    docs = list(db.collection(old_collection_name).stream())
    total_docs = len(docs)

    for i in tqdm(range(0, total_docs, BATCH_SIZE), desc="Migrating in batches"):
        batch = db.batch()
        batch_docs = docs[i : i + BATCH_SIZE]

        for doc in batch_docs:
            data = doc.to_dict()
            dest_ref = db.collection(new_collection_name).document(doc.id)
            batch.set(dest_ref, data)

        batch.commit()

    for i in tqdm(range(0, total_docs, BATCH_SIZE), desc="Deleting old documents in batches"):
        batch = db.batch()
        batch_docs = docs[i:i + BATCH_SIZE]
        for doc in batch_docs:
            batch.delete(doc.reference)
        batch.commit()


if __name__ == "__main__":
    main()
