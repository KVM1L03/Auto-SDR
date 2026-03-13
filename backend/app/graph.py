from langgraph.graph import StateGraph, START
from langgraph.constants import END

from app.agent.schema import AgentState
from app.search.service import search_node
from app.qualifier.service import qualifier_node, route_lead
from app.email.service import email_node

_compiled_graph = None


def build_sdr_graph():
    """Build and compile the SDR graph."""
    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node("search_node", search_node)
    graph.add_node("qualifier_node", qualifier_node)
    graph.add_node("email_node", email_node)

    # Edges
    graph.add_edge(START, "search_node")
    graph.add_edge("search_node", "qualifier_node")
    graph.add_conditional_edges("qualifier_node", route_lead)
    graph.add_edge("email_node", END)

    return graph.compile()


def get_sdr_graph():
    """Return cached compiled graph (singleton)."""
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_sdr_graph()
    return _compiled_graph