from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

# ✅ Load .env into environment
load_dotenv()

class Settings(BaseSettings):
    database_url: str
    openai_api_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="forbid",           # ⛔ Block unexpected fields
        populate_by_name=True     # ✅ Allows field aliases like OPENAI_API_KEY
    )

settings = Settings()
