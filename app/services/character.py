import random

from app.db_access.devices import set_character, get_character
from app.llm.character import get_random_character_for_category
from app.resources.resources import CHARACTERS, CHARACTER_IMAGE_URLS


def start_themed_game_service(db, device_id, category):
    if not category or not category.strip():
        return {"error": "Category is required."}
    if not device_id:
        return {"error": "Device ID is required."}

    character = get_random_character_for_category(db, category)
    if not character:
        return {"error": f"No character found for category '{category}'"}

    set_character(db, device_id, character)
    return {
        "message": f"Themed game started for category: {category}",
        "category": category,
        "character": character,
    }


def start_regular_game_service(db, device_id):
    if not device_id:
        return {"error": "Device ID is required."}
    character = random.choice(CHARACTERS)
    set_character(db, device_id, character)
    return {"message": "Regular game started.", "character": character}


def reveal_character_service(db, device_id):
    if not device_id:
        return {"error": "Device ID is required."}
    current_character = get_character(db, device_id)
    if not current_character:
        return {"error": "No character found for this device."}
    return {
        "character": current_character,
        "image_url": CHARACTER_IMAGE_URLS.get(current_character),
    }
