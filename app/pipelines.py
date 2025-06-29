PIPELINES = {
    "use_wikipedia": {
        "probability": 0.25,
        "use_wikipedia": True,
        "model": "gemini-2.0-flash",
    },
    "use_wikipedia_2.5": {
        "probability": 0.25,
        "use_wikipedia": True,
        "model": "gemini-2.5-flash",
    },
    "dont_use_wikipedia": {
        "probability": 0.25,
        "use_wikipedia": False,
        "model": "gemini-2.0-flash",
    },
    "dont_use_wikipedia_2.5": {
        "probability": 0.25,
        "use_wikipedia": False,
        "model": "gemini-2.5-flash",
    },
}
