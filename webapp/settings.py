import os


DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
DEBUG_USER_EMAIL = os.getenv("DEBUG_USER_EMAIL")
