import json
import os

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import FieldFilter

from app.config import config


CHARACTERS_FILE_PATH = "app/resources/characters.txt"
IMAGE_URLS_FILE_PATH = "app/resources/image_urls.json"


def initialize_firebase():
    """Initializes the Firebase Admin SDK."""
    if not firebase_admin._apps:
        cred = credentials.Certificate(config.FIREBASE_KEY_PATH)
        firebase_admin.initialize_app(cred)
    return firestore.client()


def update_firestore_character_name(db, old_name, new_name):
    """Updates the character name in the 'answers' collection in Firestore."""
    answers_ref = db.collection("answers")
    query = answers_ref.where(filter=FieldFilter("character", "==", old_name))
    results = query.get()
    for doc in results:
        doc.reference.update({"character": new_name})


def update_characters_file(old_name, new_name):
    """Updates the character name in the characters.txt file."""
    with open(CHARACTERS_FILE_PATH, "r") as f:
        lines = f.readlines()
    updated_lines = [line.replace(old_name, new_name) for line in lines]
    with open(CHARACTERS_FILE_PATH, "w") as f:
        f.writelines(updated_lines)


def update_image_urls_file(old_name, new_name):
    """Updates the character name (as a key) in the image_urls.json file."""
    with open(IMAGE_URLS_FILE_PATH, "r") as f:
        image_urls = json.load(f)
    if old_name in image_urls:
        image_urls[new_name] = image_urls.pop(old_name)
    with open(IMAGE_URLS_FILE_PATH, "w") as f:
        json.dump(image_urls, f, indent=4, sort_keys=True)


def rename_character(old_name, new_name):
    """Orchestrates the renaming of a character across different data sources."""
    db = initialize_firebase()
    update_firestore_character_name(db, old_name, new_name)
    update_characters_file(old_name, new_name)
    update_image_urls_file(old_name, new_name)


def main():
    """Main function to get user input and execute the renaming process."""
    old_character_name = input("Enter the current name of the character to rename: ")
    new_character_name = input("Enter the new name for the character: ")

    rename_character(old_character_name, new_character_name)


if __name__ == "__main__":
    main()
