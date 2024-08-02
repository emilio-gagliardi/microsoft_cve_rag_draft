from abc import ABC, abstractmethod
from typing import List, Dict


class BaseLLMClient(ABC):
    @abstractmethod
    async def get_chat_completion(
        self, messages: List[Dict[str, str]], **kwargs
    ) -> str:
        pass
