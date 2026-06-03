import json
import os
from pydantic_settings import BaseSettings


SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")


def load_settings_json() -> dict:
    """Load settings from JSON file if it exists."""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {}


class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    MODEL_NAME: str = "gpt-4o"

    VECTOR_STORE_TYPE: str = "faiss"  # faiss or iris

    IRIS_HOST: str = "http://localhost:52773"
    IRIS_NAMESPACE: str = "USER"
    IRIS_FHIR_PATH: str = "/fhir/r4"
    IRIS_USERNAME: str = "_SYSTEM"
    IRIS_PASSWORD: str = "SYS"
    IRIS_SQL_PORT: int = 1972

    class Config:
        env_file = ".env"


def reload_settings():
    """Reload settings from settings.json, merge with env vars."""
    global settings
    saved = load_settings_json()

    # Update from settings.json - use "key in saved" to allow empty values
    if "openai_api_key" in saved:
        settings.OPENAI_API_KEY = saved["openai_api_key"]
    if "openai_base_url" in saved:
        settings.OPENAI_BASE_URL = saved["openai_base_url"]
    if "model_name" in saved:
        settings.MODEL_NAME = saved["model_name"]
    if "vector_store_type" in saved:
        settings.VECTOR_STORE_TYPE = saved["vector_store_type"]
    # For IRIS host, only use settings.json if it's not localhost (Docker compatibility)
    if "iris_host" in saved and "localhost" not in saved["iris_host"]:
        settings.IRIS_HOST = saved["iris_host"]
    if "iris_namespace" in saved:
        settings.IRIS_NAMESPACE = saved["iris_namespace"]
    if "iris_fhir_path" in saved:
        settings.IRIS_FHIR_PATH = saved["iris_fhir_path"]
    if "iris_username" in saved:
        settings.IRIS_USERNAME = saved["iris_username"]
    if "iris_password" in saved:
        settings.IRIS_PASSWORD = saved["iris_password"]
    if "iris_sql_port" in saved:
        settings.IRIS_SQL_PORT = saved["iris_sql_port"]

    return settings


# Initialize settings - Pydantic loads from env vars and .env file
# settings.json overrides are only applied via reload_settings()
settings = Settings()
