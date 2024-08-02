from typing import List, Dict, Any
from .llm_factory import get_llm_client
from services.embedding_service import get_embedding_service
from arize.phoenix.logger import Logger  # Placeholder import for Arize Phoenix

# Initialize Arize Phoenix logger
phoenix_logger = Logger()  # Placeholder initialization


async def get_chat_completion(
    provider: str, config: Dict[str, Any], messages: List[Dict[str, str]], **kwargs
) -> str:
    client = get_llm_client(provider, config)

    # Arize Phoenix logging - start
    trace_id = phoenix_logger.start_trace(
        model_name=f"{provider}_chat_model", inputs={"messages": messages, **kwargs}
    )

    try:
        response = await client.get_chat_completion(messages, **kwargs)

        # Arize Phoenix logging - success
        phoenix_logger.log_response(
            trace_id=trace_id, output=response, status="success"
        )

        return response
    except Exception as e:
        # Arize Phoenix logging - error
        phoenix_logger.log_response(trace_id=trace_id, output=str(e), status="error")
        raise e


async def get_embedding(
    provider: str, config: Dict[str, Any], text: str
) -> List[float]:
    embedding_service = get_embedding_service(provider, config)
    return await embedding_service.get_embedding(text)


if __name__ == "__main__":
    query = input("Enter your query: ")
    print(query)
