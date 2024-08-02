# services/embedding_service.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseEmbeddingService(ABC):
    @abstractmethod
    async def get_embedding(self, text: str) -> List[float]:
        pass


class OpenAIEmbeddingService(BaseEmbeddingService):
    def __init__(self, config: Dict[str, Any]):
        import openai

        openai.api_key = config["api_key"]
        self.client = openai

    async def get_embedding(self, text: str) -> List[float]:
        response = await self.client.Embedding.acreate(
            input=text, model="text-embedding-ada-002"
        )
        return response["data"][0]["embedding"]


class OllamaEmbeddingService(BaseEmbeddingService):
    def __init__(self, config: Dict[str, Any]):
        self.base_url = config.get("base_url", "http://localhost:11434")
        self.model = config.get("model", "llama2")

    async def get_embedding(self, text: str) -> List[float]:
        import httpx

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/embeddings",
                json={"model": self.model, "prompt": text},
            )
            return response.json()["embedding"]


def get_embedding_service(
    provider: str, config: Dict[str, Any]
) -> BaseEmbeddingService:
    if provider == "openai":
        return OpenAIEmbeddingService(config)
    elif provider == "ollama":
        return OllamaEmbeddingService(config)
    else:
        raise ValueError(f"Unsupported embedding provider: {provider}")
