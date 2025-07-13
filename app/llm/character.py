import google.generativeai as genai

from app.llm.gemini import models, timeout


@timeout(10)
def get_random_character_for_category(db, category):
    """
    Use Gemini to generate a random character name for the given category.
    Returns the character name as a string, or None if not found.
    """
    prompt = f"Give me the name of a famous {category} character or person. Only return the name."
    # Use a default model for this simple generation
    model_name = "gemini-2.0-flash"
    response = models[model_name].generate_content(
        contents=prompt,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=16,
            temperature=1.0,
            top_p=1,
            top_k=1,
        ),
        stream=False,
    )
    # Try to extract the name from the response
    if hasattr(response, "text"):
        name = response.text.strip()
    elif hasattr(response, "candidates") and response.candidates:
        name = response.candidates[0].content.parts[0].text.strip()
    else:
        return None
    # Remove any extra explanations or punctuation
    name = name.split("\n")[0].strip().strip(".").strip('"')
    if not name:
        return None
    return name
