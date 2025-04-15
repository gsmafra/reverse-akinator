import wikipedia
from sentry_sdk import capture_exception
from app.resources.resources import WIKIPEDIA_PAGES

_wikipedia_cache = {}


def get_wikipedia_article(character):
    """Retrieves a Wikipedia article from the cache.
    If not found, it fetches and caches it.
    """
    title = WIKIPEDIA_PAGES.get(character, character)
    if title in _wikipedia_cache:
        return _wikipedia_cache[title]

    try:
        print(f"Fetching Wikipedia content for: {title}")
        page = wikipedia.page(title, auto_suggest=False)
        _wikipedia_cache[title] = page.content
        return page.content
    except wikipedia.exceptions.PageError:
        print(f"Error: Page not found for {title}")
        capture_exception(e)
        return None
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"Error: Disambiguation for {title}: {e.options}")
        capture_exception(e)
        return None
