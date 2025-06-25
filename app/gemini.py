import concurrent.futures
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
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(func, *args, **kwargs)
                try:
                    return future.result(timeout=seconds)
                except concurrent.futures.TimeoutError as exc:
                    raise TimeoutError(
                        f"Function call timed out after {seconds} seconds"
                    ) from exc

        return wrapper

    return decorator


def _parse_gemini_response(response):
    if not response or not response.candidates:
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
        return f"Invalid answer format: '{first_part.text}'"

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
