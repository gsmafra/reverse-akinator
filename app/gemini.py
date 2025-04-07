import google.generativeai as genai

from app.config import config
from app.resources.resources import PROMPT_TEMPLATE

genai.configure(api_key=config.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


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

    answer = first_part.text.strip()  # Remove potential whitespace

    if answer.lower() not in ["yes", "no", "ambiguous"]:
        return f"Invalid answer format: '{answer}'"

    return answer.lower()


def get_gemini_answer(character, question):
    prompt = PROMPT_TEMPLATE.replace("{{character}}", character).replace(
        "{{question}}", question
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
