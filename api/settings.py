import json
import os
from fastapi import APIRouter
from pydantic import BaseModel
from config import reload_settings

router = APIRouter()

SETTINGS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "settings.json")


class SettingsData(BaseModel):
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    model_name: str = "gpt-4o"
    vector_store_type: str = "faiss"
    iris_host: str = "http://localhost:52773"
    iris_namespace: str = "USER"
    iris_fhir_path: str = "/fhir/r4"
    iris_username: str = "_system"
    iris_password: str = "SYS"
    iris_sql_port: int = 1972


@router.get("/api/settings")
def get_settings():
    from config import settings
    return {
        "openai_api_key": settings.OPENAI_API_KEY,
        "openai_base_url": settings.OPENAI_BASE_URL,
        "model_name": settings.MODEL_NAME,
        "vector_store_type": settings.VECTOR_STORE_TYPE,
        "iris_host": settings.IRIS_HOST,
        "iris_namespace": settings.IRIS_NAMESPACE,
        "iris_fhir_path": settings.IRIS_FHIR_PATH,
        "iris_username": settings.IRIS_USERNAME,
        "iris_password": settings.IRIS_PASSWORD,
        "iris_sql_port": settings.IRIS_SQL_PORT,
    }


@router.post("/api/settings")
def update_settings(data: SettingsData):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data.model_dump(), f, indent=2)

    # Reload settings immediately
    reload_settings()

    return {"status": "ok", "message": "Settings applied successfully"}


@router.post("/api/vectorstore/rebuild")
def rebuild_vectorstore():
    """Rebuild vectorstore with current settings."""
    try:
        from services.rag_service import build_vectorstore
        result = build_vectorstore()
        return {"status": "ok", "message": f"Vectorstore rebuilt successfully", "result": str(result)}
    except Exception as e:
        return {"status": "error", "message": str(e)}
