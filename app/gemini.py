import threading
from functools import wraps

import google.generativeai as genai

from app.config import config
from app.resources.resources import PROMPT_TEMPLATE
from app.wikipedia import get_wikipedia_article

genai.configure(api_key=config.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")


def timeout(seconds):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = [None]
            exception = [None]
            finished = threading.Event()

            def target():
                # pylint: disable=W0718
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e
                finally:
                    finished.set()

            thread = threading.Thread(target=target)
            thread.daemon = (
                True  # Allow the main thread to exit even if this thread is running
            )
            thread.start()
            finished.wait(timeout=seconds)

            if not finished.is_set():
                raise TimeoutError(f"Function call timed out after {seconds} seconds")
            if exception[0]:
                # pylint: disable=E0702
                raise exception[0]
            return result[0]

        return wrapper

    return decorator


def _parse_gemini_response(response):
    if not response.candidates:
        return "No response from the model"

    first_candidate = response.candidates[0]

    if not first_candidate.content:
        return "No content in the first candidate"
    if not first_candidate.content.parts:
        return "No content parts in the first candidate"

    first_part = first_candidate.content.parts[0]

    if not first_part.text:
        return "No text in the first part of the first candidate"

    answer = first_part.text.strip().lower()

    if answer == "amb":
        answer = "ambiguous"

    if answer not in ["yes", "no", "ambiguous"]:
        return f"Invalid answer format: '{answer}'"

    return answer


@timeout(10)
def get_gemini_answer(character, question):
    wikipedia_page = get_wikipedia_article(character)
    prompt = (
        PROMPT_TEMPLATE.replace("{{character}}", character)
        .replace("{{question}}", question)
        .replace("{{wikipedia_page}}", wikipedia_page)
    )
    response = model.generate_content(
        contents=prompt,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=1,
            temperature=0,
            top_p=1,
            top_k=1,
        ),
        stream=False,
    )
    answer = _parse_gemini_response(response)
    return answer
