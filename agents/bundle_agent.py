from services.llm_service import get_llm


def bundle_node(state):

    question = state["question"]
    context = state.get("context", "")

    prompt = f"""
Generate a FHIR Bundle.
Use the following FHIR documentation as reference:
{context}

Include relevant resources such as:
Patient, Encounter, Condition, Observation

Scenario: {question}

Return valid FHIR Bundle JSON only.
"""

    state["result"] = get_llm().invoke(prompt).content

    return state
