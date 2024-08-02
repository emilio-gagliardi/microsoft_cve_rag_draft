from pydantic import BaseModel
from typing import Optional


class ETLRunResponse(BaseModel):
    message: str


class GenerateEmbeddingsRequest(BaseModel):
    data: dict


class GenerateEmbeddingsResponse(BaseModel):
    embeddings: dict
