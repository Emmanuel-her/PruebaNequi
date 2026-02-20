import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = os.getenv("Api chat nequi", "Api chat nequi")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./chat.db")

settings = Settings()
