import os
from dotenv import load_dotenv

from pathlib import Path
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME: str = 'Shorten URL App'
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: int = os.getenv("POSTGRES_PORT", 5432)
    POSTGTRES_DB: str = os.getenv("POSTGRES_DB")

    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGTRES_DB}"
    SECRET_KEY: str = os.getenv("SECRET_KEY")


settings = Settings()