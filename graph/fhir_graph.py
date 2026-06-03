from langgraph.graph import StateGraph, END

from agents.state import AgentState
from agents.router_agent import router_node
from agents.rag_agent import rag_node
from agents.expert_agent import expert_node
from agents.query_agent import query_node
from agents.mapping_agent import mapping_node
from agents.bundle_agent import bundle_node
from agents.validation_agent import validation_node
from agents.iris_agent import iris_node


graph = StateGraph(AgentState)

graph.add_node("router", router_node)
graph.add_node("rag", rag_node)
graph.add_node("expert", expert_node)
graph.add_node("query", query_node)
graph.add_node("mapping", mapping_node)
graph.add_node("bundle", bundle_node)
graph.add_node("validation", validation_node)
graph.add_node("iris", iris_node)

graph.set_entry_point("router")

# Router -> RAG (always)
graph.add_edge("router", "rag")


def rag_route(state):
    return state["task_type"]


# RAG -> appropriate agent based on task_type
graph.add_conditional_edges(
    "rag",
    rag_route,
    {
        "expert": "expert",
        "query": "query",
        "mapping": "mapping",
        "bundle": "bundle",
        "validation": "validation",
        "iris": "iris",
    },
)

graph.add_edge("expert", END)
graph.add_edge("query", END)
graph.add_edge("mapping", END)
graph.add_edge("bundle", END)
graph.add_edge("validation", END)
graph.add_edge("iris", END)

app_graph = graph.compile()
