PIPELINES = {
    "use_wikipedia": {
        "probability": 0.25,
        "use_wikipedia": True,
        "model": "gemini-2.0-flash",
        "use_character_question_hint": False,
    },
    "use_wikipedia_2.5": {
        "probability": 0.25,
        "use_wikipedia": True,
        "model": "gemini-2.5-flash",
        "use_character_question_hint": False,
    },
    "dont_use_wikipedia": {
        "probability": 0,
        "use_wikipedia": False,
        "model": "gemini-2.0-flash",
        "use_character_question_hint": False,
    },
    "dont_use_wikipedia_2.5": {
        "probability": 0.25,
        "use_wikipedia": False,
        "model": "gemini-2.5-flash",
        "use_character_question_hint": False,
    },
    "nowiki_character_question_hint": {
        "probability": 0.25,
        "use_wikipedia": False,
        "model": "gemini-2.5-flash",
        "use_character_question_hint": True,
    },
}
