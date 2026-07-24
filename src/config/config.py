from dotenv import load_dotenv
import os

load_dotenv(override=True)

class Settings:

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    GEMINI_MODEL = "gemini-2.5-flash"

    UPLOAD_FOLDER = "uploads"

settings = Settings()