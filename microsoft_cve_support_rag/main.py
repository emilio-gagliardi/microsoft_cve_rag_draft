# from langtrace_python_sdk import langtrace
import os
import sys
import yaml

from app_utils import (
    get_openai_api_key,
)
import logging

os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"
os.environ["OPENAI_API_KEY"] = get_openai_api_key()

# Get the logger instance
logger = logging.getLogger(__name__)


def load_yaml(yaml_path):
    with open(yaml_path, "r") as file:
        logger.info("Loading input data...")
        return yaml.safe_load(file)


def run():
    # inputs are loaded from yaml
    yaml_path = "parameters.yml"
    startup_parameters = load_yaml(yaml_path)
    logger.info(f"starting up app. Loading application settings:\n{startup_parameters}")
    print("foo")


def train():
    yaml_path = "job_inputs.yml"
    inputs = load_yaml(yaml_path)
    logger.info("crew train initiate ...")
    print(f"terminal input = {sys.argv[1]}\nyaml inputs = \n{inputs}")


if __name__ == "__main__":

    print("## Welcome to the CVE RAG app")
    print("-------------------------------")
    run()
