import openai
import httpx
from typing import List, Dict, Any
from .llm_interface import BaseLLMClient


class OpenAILLMClient(BaseLLMClient):
    def __init__(self, api_key: str):
        openai.api_key = api_key

    async def get_chat_completion(
        self, messages: List[Dict[str, str]], **kwargs
    ) -> str:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo", messages=messages, **kwargs
        )
        return response.choices[0].message.content

    async def get_embedding(self, text: str) -> List[float]:
        response = await openai.Embedding.acreate(
            input=text, model="text-embedding-ada-002"
        )
        return response["data"][0]["embedding"]


class OllamaLLMClient(BaseLLMClient):
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url)

    async def get_chat_completion(
        self, messages: List[Dict[str, str]], **kwargs
    ) -> str:
        response = await self.client.post(
            "/api/chat", json={"messages": messages, **kwargs}
        )
        return response.json()["message"]["content"]

    async def get_embedding(self, text: str) -> List[float]:
        response = await self.client.post("/api/embeddings", json={"input": text})
        return response.json()["embedding"]


class GroqLLMClient(BaseLLMClient):
    def __init__(self, api_key: str):
        self.client = httpx.AsyncClient(
            base_url="https://api.groq.com/v1",
            headers={"Authorization": f"Bearer {api_key}"},
        )

    async def get_chat_completion(
        self, messages: List[Dict[str, str]], **kwargs
    ) -> str:
        response = await self.client.post(
            "/chat/completions", json={"messages": messages, **kwargs}
        )
        return response.json()["choices"][0]["message"]["content"]

    async def get_embedding(self, text: str) -> List[float]:
        response = await self.client.post("/embeddings", json={"input": text})
        return response.json()["data"][0]["embedding"]
