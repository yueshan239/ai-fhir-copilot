from typing import TypedDict


class AgentState(TypedDict):
    question: str
    task_type: str
    context: str
    result: str
