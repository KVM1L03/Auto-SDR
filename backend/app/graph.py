from langgraph.graph import StateGraph, START
from langgraph.constants import END

from app.agent.schema import AgentState
from app.search.service import search_node
from app.qualifier.service import qualifier_node, route_lead

def email_node(state: AgentState) -> dict:
    return {"draft_email": ""}

def build_sdr_graph():
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