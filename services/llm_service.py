from langchain_openai import ChatOpenAI
from config import settings


def get_llm():
    """Get LLM instance with current settings."""
    return ChatOpenAI(
        model=settings.MODEL_NAME,
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
        temperature=0.1,
    )
