import json
from services.llm_service import get_llm


def validation_node(state):

    try:

        data = json.loads(state["question"])

        if "resourceType" not in data:

            state["result"] = "Invalid Resource: resourceType missing"
            return state

        context = state.get("context", "")

        prompt = f"""
Validate this FHIR resource.
Use the following validation rules as reference:
{context}

Resource:
{state['question']}

Return:
1. Valid or Invalid
2. Issues found (if any)
3. Suggestions for improvement
"""

        state["result"] = get_llm().invoke(prompt).content

    except json.JSONDecodeError as e:

        state["result"] = f"Invalid JSON: {str(e)}"

    except Exception as e:

        state["result"] = str(e)

    return state
