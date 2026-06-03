from services.llm_service import get_llm


def router_node(state):

    question = state["question"]

    prompt = f"""
You are a FHIR task router.

Classify the request into exactly ONE of these types:

expert - FHIR questions, concepts, explanations
query - Natural language to FHIR search API
mapping - Convert JSON to FHIR resource
bundle - Generate FHIR Bundle
validation - Validate FHIR resource
iris - Fetch/store data from IRIS FHIR server

Return ONLY the type name, nothing else.

Question:
{question}
"""

    result = get_llm().invoke(prompt).content.strip().lower()

    # Clean up - extract just the type if LLM returns extra text
    for valid_type in ["expert", "query", "mapping", "bundle", "validation", "iris"]:
        if valid_type in result:
            result = valid_type
            break

    state["task_type"] = result

    return state
