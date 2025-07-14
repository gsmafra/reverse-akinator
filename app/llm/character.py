import random

import google.generativeai as genai

from app.llm.gemini import models, timeout


@timeout(10)
def get_random_character_for_category(db, category):
    """
    Use Gemini to generate a list of 50 famous characters/people for the given category, then pick one at random.
    Returns the character name as a string, or None if not found.
    """
    prompt = (
        f"List 50 different famous {category} characters or people. "
        "Return only a comma-separated list of names, no numbers or explanations."
    )
    model_name = "gemini-2.0-flash"
    response = models[model_name].generate_content(
        contents=prompt,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=256,
            temperature=1.2,
            top_p=1,
            top_k=40,
        ),
        stream=False,
    )
    # Try to extract the list from the response
    if hasattr(response, "text"):
        names_text = response.text.strip()
    elif hasattr(response, "candidates") and response.candidates:
        names_text = response.candidates[0].content.parts[0].text.strip()
    else:
        return None
    # Split and clean names
    names = [n.strip().strip(".") for n in names_text.split(",") if n.strip()]
    if not names:
        return None
    return random.choice(names)
