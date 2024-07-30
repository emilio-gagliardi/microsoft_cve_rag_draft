# from langtrace_python_sdk import langtrace
import os
import sys
import yaml

from app_utils import (
    get_openai_api_key,
    get_vector_db_credentials,
    get_graph_db_credentials,
)
import logging

os.environ["OPENAI_MODEL_NAME"] = "gpt-4o-mini"
os.environ["OPENAI_API_KEY"] = get_openai_api_key()

# Get the logger instance
logger = logging.getLogger(__name__)


def run():

    print("Hello world from application main")


if __name__ == "__main__":
    vector_credentials = get_vector_db_credentials()
    print(f"The vector credentials:\n{vector_credentials}")

    # graph_credentials = get_graph_db_credentials()
    # print(f"The graph credentials:\n{graph_credentials}")
    run()
    # documents_credentials = get_documents_db_credentials()
    # print(documents_credentials)
