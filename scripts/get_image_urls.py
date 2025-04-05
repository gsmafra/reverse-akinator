import json
from os import environ

from google_images_search import GoogleImagesSearch
from tqdm import tqdm

from app.resources.resources import CHARACTERS, CHARACTER_IMAGE_URLS


def search_for_image_in_google(query):
    """
    Searches for images on the web using the Google Images Search API.

    Args:
        query (str): The search term (e.g., "Mickey Mouse").
        size (str, optional): Filter by image size (e.g., 'large', 'medium', 'icon'). Defaults to None.

    Returns:
        list: A list of dictionaries, where each dictionary represents an image result.
              Each dictionary typically contains keys like 'url', 'height', 'width', 'title', etc.
              Returns an empty list if no results are found or if there's an API error.
    """
    gis = GoogleImagesSearch(
        environ["GOOGLE_SEARCH_API_KEY"], environ["GOOGLE_SEARCH_ENGINE_ID"]
    )

    search_params = {
        "q": query,
        "num": 1,
        "safe": "active",
        "fileType": "jpg",
        "imgSize": "medium",
    }

    gis.search(search_params=search_params)
    return gis.results()[0].url


def main():
    url_dict = CHARACTER_IMAGE_URLS.copy()
    for character in tqdm(CHARACTERS):
        if character in url_dict:
            continue
        url = search_for_image_in_google(character)
        print(url)
        url_dict[character] = url
        with open("app/resources/image_urls.json", "w") as f:
            json.dump(url_dict, f, indent=4)


if __name__ == "__main__":
    main()
