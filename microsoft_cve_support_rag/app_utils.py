import os
from dotenv import load_dotenv, find_dotenv
import logging

# Configure the logger
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),
    ],
)

# Create a logger object
logger = logging.getLogger(__name__)

env_loaded = False


def load_env():
    global env_loaded

    if env_loaded:
        return  # Environment variables are already loaded

    environment = os.getenv("ENVIRONMENT", "local")
    # environment = "production"
    # Map environment to the correct .env file
    env_file_map = {
        "local": ".env.local",
        "docker": ".env.docker",
    }
    dotenv_file = env_file_map.get(environment)
    if dotenv_file is None:
        raise ValueError(
            f"Environment '{environment}' is not recognized. Please set up the environment before using the app."
        )

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    dotenv_path = os.path.join(project_root, dotenv_file)

    if not os.path.exists(dotenv_path):
        raise FileNotFoundError(f"The .env file at path {dotenv_path} does not exist.")

    if load_dotenv(dotenv_path):
        logging.info(f"Environment variable(s) loaded successfully from {dotenv_file}")
        env_loaded = True
    else:
        logging.warning(f"No {dotenv_file} file found or failed to load")
        env_loaded = False


def get_openai_api_key():
    load_env()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key is None:
        logging.error("OPENAI_API_KEY environment variable is not set")
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return openai_api_key


def get_serper_api_key():
    load_env()
    serper_api_key = os.getenv("SERPER_API_KEY")
    if serper_api_key is None:
        logging.error("SERPER_API_KEY environment variable is not set")
        raise ValueError("SERPER_API_KEY environment variable is not set")
    return serper_api_key


def get_groq_api_key():
    load_env()
    groq_api_key = os.getenv("GROQ_API_KEY")
    if groq_api_key is None:
        logging.error("GROQ_API_KEY environment variable is not set")
        raise ValueError("GROQ_API_KEY environment variable is not set")
    return groq_api_key


def get_exa_api_key():
    load_env()
    exa_api_key = os.getenv("EXA_API_KEY")
    if exa_api_key is None:
        logging.error("EXA_API_KEY environment variable is not set")
        raise ValueError("EXA_API_KEY environment variable is not set")
    return exa_api_key


def get_notion_api_key():
    load_env()
    notion_api_key = os.getenv("NOTION_API_KEY")
    if notion_api_key is None:
        logging.error("NOTION_API_KEY environment variable is not set")
        raise ValueError("NOTION_API_KEY environment variable is not set")
    return notion_api_key


def get_tavily_api_key():
    load_env()
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if tavily_api_key is None:
        logging.error("TAVILY_API_KEY environment variable is not set")
        raise ValueError("TAVILY_API_KEY environment variable is not set")
    return tavily_api_key


def get_langtrace_api_key():
    load_env()
    langtrace_api_key = os.getenv("LANGTRACE_API_KEY")
    if langtrace_api_key is None:
        logging.error("LANGTRACE_API_KEY environment variable is not set")
        raise ValueError("LANGTRACE_API_KEY environment variable is not set")
    return langtrace_api_key
