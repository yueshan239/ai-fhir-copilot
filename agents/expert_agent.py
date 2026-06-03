from services.llm_service import get_llm


def expert_node(state):

    question = state["question"]
    context = state.get("context", "")

    prompt = f"""
You are a HL7 FHIR expert.
Use the following FHIR documentation to answer.

Context:
{context}

Question: {question}
"""

    state["result"] = get_llm().invoke(prompt).content

    return state
