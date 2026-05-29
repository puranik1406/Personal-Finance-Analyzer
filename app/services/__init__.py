from app.services import db_service
from app.services.ollama_service import OllamaService

ollama_service = OllamaService()

__all__ = ["db_service", "ollama_service"]
