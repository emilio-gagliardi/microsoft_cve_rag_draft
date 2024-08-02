from fastapi import APIRouter
from chat.main_chat import chat

from schemas.chat_schemas import (
    ChatQueryRequest,
    ChatQueryResponse,
    GenerateCompletionRequest,
    GenerateCompletionResponse,
    EmbeddingRequest,
    EmbeddingResponse,
)

router = APIRouter()


@router.post("/query", response_model=ChatQueryResponse)
def query_chat(request: ChatQueryRequest):
    response = chat(request.query)
    return ChatQueryResponse(response=response)


@router.post("/generate-completion", response_model=GenerateCompletionResponse)
def generate_chat_completion(request: GenerateCompletionRequest):
    completion = generate_completion(request.data)
    return GenerateCompletionResponse(completion=completion)


@router.post("/embedding", response_model=EmbeddingResponse)
async def get_text_embedding(request: EmbeddingRequest):
    try:
        provider = request.provider  # Get provider from request
        config = get_embedding_config(
            provider
        )  # Implement this function to get config based on provider
        embedding = await get_embedding(provider, config, request.text)
        return EmbeddingResponse(embedding=embedding)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
