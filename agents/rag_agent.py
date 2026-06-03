from services.rag_service import search


def rag_node(state):
    results = search(state["question"], k=3)
    state["context"] = "\n---\n".join(results)
    return state
