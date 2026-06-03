from services.llm_service import get_llm


def mapping_node(state):

    source = state["question"]
    context = state.get("context", "")

    prompt = f"""
Convert source JSON to FHIR resource.
Use the following FHIR resource documentation as reference:
{context}

Source:
{source}

Return valid FHIR JSON only.
"""

    state["result"] = get_llm().invoke(prompt).content

    return state
