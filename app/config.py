import os

class Config:
    FIREBASE_KEY_PATH = os.environ.get("AKINATOR_FIREBASE_KEY_PATH")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    DEBUG = True

config = Config()
