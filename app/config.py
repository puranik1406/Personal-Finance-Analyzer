import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ollama_base_url: str = "http://localhost:11434"
    default_model: str = "gemma:2b"
    database_url: str = "sqlite:///./finance.db"
    port: int = 5000
    host: str = "127.0.0.1"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
