import textwrap

from app.llm.wikipedia import get_wikipedia_article
from app.resources.resources import PROMPT_TEMPLATE


def build_gemini_prompt(character, question, pipeline_config):
    """
    Build the prompt for Gemini model using the template and provided fields and pipeline config.
    """
    use_wikipedia = pipeline_config.get("use_wikipedia", False)
    use_character_question_hint = pipeline_config.get("use_character_question_hint", "")

    if use_wikipedia:
        wikipedia_page = get_wikipedia_article(character)
    else:
        wikipedia_page = "No Wikipedia page available for this character."

    if use_character_question_hint:
        character_question_hint = textwrap.dedent(
            """
            If the question is simply a character, answer yes/no depending on whether the character is correct.

            Example:
            character: Darth Vader
            question: Darth Vader
            → yes

            character: Darth Vader
            question: Luke Skywalker
            → no
        """
        ).strip()
    else:
        character_question_hint = ""

    return (
        PROMPT_TEMPLATE.replace("{{character}}", character)
        .replace("{{question}}", question)
        .replace("{{wikipedia_page}}", wikipedia_page)
        .replace("{{character_question_hint}}", character_question_hint)
    )
