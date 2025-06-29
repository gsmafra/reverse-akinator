import concurrent.futures
from functools import wraps
import random

import google.generativeai as genai

from app.config import config
from app.pipelines import PIPELINES
from app.resources.resources import PROMPT_TEMPLATE
from app.wikipedia import get_wikipedia_article

genai.configure(api_key=config.GEMINI_API_KEY)
MODEL_NAMES = [
    "gemini-2.0-flash",
    "gemini-2.5-flash",
]

models = {name: genai.GenerativeModel(name) for name in MODEL_NAMES}


def timeout(seconds):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(func, *args, **kwargs)
                try:
                    return future.result(timeout=seconds)
                except concurrent.futures.TimeoutError as exc:
                    raise TimeoutError(f"Function call timed out after {seconds} seconds") from exc

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


def _choose_pipeline():
    pipelines = list(PIPELINES.items())
    names = [name for name, _ in pipelines]
    probabilities = [PIPELINES[name]["probability"] for name in names]
    pipeline_name = random.choices(names, weights=probabilities, k=1)[0]
    return pipeline_name, PIPELINES[pipeline_name]


@timeout(10)
def get_gemini_answer(character, question):
    # Choose pipeline based on probabilities
    pipeline_name, pipeline_config = _choose_pipeline()
    use_wikipedia = pipeline_config.get("use_wikipedia", False)
    model_name = pipeline_config.get("model", "gemini-2.0-flash")

    if use_wikipedia:
        wikipedia_page = get_wikipedia_article(character)
    else:
        wikipedia_page = "No Wikipedia page available for this character."

    prompt = (
        PROMPT_TEMPLATE.replace("{{character}}", character)
        .replace("{{question}}", question)
        .replace("{{wikipedia_page}}", wikipedia_page)
    )
    response = models[model_name].generate_content(
        contents=prompt,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=1 if model_name == "gemini-2.0-flash" else None,
            temperature=0,
            top_p=1,
            top_k=1,
        ),
        stream=False,
    )
    answer = _parse_gemini_response(response)

    if answer not in ["yes", "no", "ambiguous"]:
        print(response)

    # Return the answer and the pipeline name for tracking
    return answer, pipeline_name
