from typing import Dict, Any
from fastapi import HTTPException
from .llm_clients import OpenAILLMClient, OllamaLLMClient, GroqLLMClient
from .llm_interface import BaseLLMClient


def get_llm_client(provider: str, config: Dict[str, Any]) -> BaseLLMClient:
    if provider == "openai":
        return OpenAILLMClient(api_key=config["api_key"])
    elif provider == "ollama":
        return OllamaLLMClient(base_url=config["base_url"])
    elif provider == "groq":
        return GroqLLMClient(api_key=config["api_key"])
    else:
        raise HTTPException(status_code=400, detail="Invalid LLM provider")
