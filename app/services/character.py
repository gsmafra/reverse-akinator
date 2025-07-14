import os
import json
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


def get_image_url_for_character(character):
    # Try to get from CHARACTER_IMAGE_URLS first
    url = CHARACTER_IMAGE_URLS.get(character)
    if url:
        return url
    # If not found, search Google Images
    from google_images_search import GoogleImagesSearch

    api_key = os.environ.get("GOOGLE_SEARCH_API_KEY")
    engine_id = os.environ.get("GOOGLE_SEARCH_ENGINE_ID")
    if not api_key or not engine_id:
        return None
    gis = GoogleImagesSearch(api_key, engine_id)
    search_params = {
        "q": character,
        "num": 1,
        "safe": "active",
        "imgSize": "medium",
    }
    try:
        gis.search(search_params=search_params)
        url = gis.results()[0].url
        # Optionally update the JSON file for future use
        CHARACTER_IMAGE_URLS[character] = url
        with open("app/resources/image_urls.json", "w", encoding="utf-8") as f:
            json.dump(CHARACTER_IMAGE_URLS, f, indent=4, sort_keys=True)
        return url
    except Exception as e:
        print(f"Error fetching image for {character}: {e}")
        return None


def reveal_character_service(db, device_id):
    if not device_id:
        return {"error": "Device ID is required."}
    current_character = get_character(db, device_id)
    if not current_character:
        return {"error": "No character found for this device."}
    image_url = get_image_url_for_character(current_character)
    return {
        "character": current_character,
        "image_url": image_url,
    }
