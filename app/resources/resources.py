import json


def read_text_file_shortest(filepath):
    with open(filepath, "r") as file:
        return file.read().splitlines()


CHARACTERS = read_text_file_shortest("app/resources/characters.txt")
with open("app/resources/image_urls.json", "r") as f:
    CHARACTER_IMAGE_URLS = json.load(f)
