from fastapi import APIRouter
from pydantic import BaseModel

from graph.fhir_graph import app_graph
from config import settings

router = APIRouter(
    prefix="/api/copilot",
    tags=["FHIR Copilot"],
)


class CopilotRequest(BaseModel):
    question: str


@router.post("")
def copilot(req: CopilotRequest):
    # Check if API key is configured
    if not settings.OPENAI_API_KEY:
        return {
            "question": req.question,
            "task_type": "error",
            "context": "",
            "result": "Please configure your OpenAI API key in Settings first. Click the gear icon (⚙) in the top right corner to open settings.",
        }

    result = app_graph.invoke(
        {
            "question": req.question,
            "task_type": "",
            "context": "",
            "result": "",
        }
    )

    return result
