import os


class Config:
    # pylint: disable=R0903
    FIREBASE_KEY_PATH = os.environ.get("AKINATOR_FIREBASE_KEY_PATH")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    SENTRY_DSN = os.environ.get("SENTRY_DSN")
    ENVIRONMENT = os.environ.get("ENVIRONMENT", "unset")
    DEBUG = True
    SCHEDULER_ENABLED = os.environ.get("SCHEDULER_ENABLED", False)


config = Config()
