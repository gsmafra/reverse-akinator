import json


def read_text_file_shortest(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read().splitlines()


CHARACTERS = read_text_file_shortest("app/resources/characters.txt")
with open("app/resources/image_urls.json", "r", encoding="utf-8") as f:
    CHARACTER_IMAGE_URLS = json.load(f)

with open("app/resources/wikipedia_pages.json", "r", encoding="utf-8") as f:
    WIKIPEDIA_PAGES = json.load(f)

with open("app/resources/prompt_template.txt", "r", encoding="utf-8") as f:
    PROMPT_TEMPLATE = f.read()
