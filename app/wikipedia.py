from functools import lru_cache

import wikipedia
from sentry_sdk import capture_exception
from app.resources.resources import WIKIPEDIA_PAGES


@lru_cache(maxsize=128)
def _fetch_wikipedia_content(title):
    print(f"Fetching Wikipedia content for: {title}")
    page = wikipedia.page(title, auto_suggest=False)
    return page.content


def get_wikipedia_article(character):
    title = WIKIPEDIA_PAGES.get(character, character)
    try:
        return _fetch_wikipedia_content(title)
    except wikipedia.exceptions.PageError as e:
        print(f"Error: Page not found for {title}")
        capture_exception(e)
        return None
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"Error: Disambiguation for {title}: {e.options}")
        capture_exception(e)
        return None
