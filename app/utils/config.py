"""Configuration helpers."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    OLLAMA_BASE_URL: str | None = None
    OLLAMA_MODEL: str | None = None

    GROQ_API_KEY: str | None = None
    GROQ_MODEL: str | None = None
    GROQ_BASE_URL: str | None = None

    CHROMA_DB_PATH: str

    LOG_LEVEL: str = "INFO"

    ENV: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()