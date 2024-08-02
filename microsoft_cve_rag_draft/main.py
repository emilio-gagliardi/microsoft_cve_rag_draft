import os
import logging
from fastapi import FastAPI
import uvicorn

from app_utils import (
    get_openai_api_key,
    get_vector_db_credentials,
    get_graph_db_credentials,
    get_documents_db_credentials,
    get_sql_db_credentials,
)
from routes.chat_routes import router as chat_router
from routes.document_routes import router as document_router
from routes.etl_routes import router as etl_router
from routes.graph_routes import router as graph_router
from routes.vector_routes import router as vector_router

# Set environment variables
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o-mini"
os.environ["OPENAI_API_KEY"] = get_openai_api_key()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the FastAPI application
app = FastAPI()

# Include routers
app.include_router(chat_router, prefix="/chat", tags=["Chat"])
app.include_router(document_router, prefix="/documents", tags=["Documents"])
app.include_router(etl_router, prefix="/etl", tags=["ETL"])
app.include_router(graph_router, prefix="/graph", tags=["Graph"])
app.include_router(vector_router, prefix="/vector", tags=["Vector"])


# Test function to print credentials
def print_credentials():
    vector_credentials = get_vector_db_credentials()
    logger.info(f"The vector db credentials:\n{vector_credentials}")

    graph_credentials = get_graph_db_credentials()
    logger.info(f"The graph db credentials:\n{graph_credentials}")

    documents_credentials = get_documents_db_credentials()
    logger.info(f"The documents db credentials:\n{documents_credentials}")

    sql_credentials = get_sql_db_credentials()
    logger.info(f"The sql db credentials:\n{sql_credentials}")


# Main function to run the application
def run():
    print_credentials()
    logger.info("Starting FastAPI application...")


if __name__ == "__main__":
    run()
    uvicorn.run(app, host="0.0.0.0", port=8000)
