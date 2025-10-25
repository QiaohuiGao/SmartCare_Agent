"""
ReAct Tools
-----------
Restricted set of callable actions for reasoning.
"""
from retriever import retrieve_kb
from graph_engine import get_step, verify_expected, advance_state

def tool_search_kb(query, filters):
    """Retrieve KB docs for reasoning."""
    return retrieve_kb(query, filters)

def tool_get_step(graph, node_id):
    """Access step by ID."""
    return get_step(graph, node_id)

def tool_record_obs(obs_store, key, value, conf=1.0):
    """Store observations from user or sensors."""
    obs_store[key] = value

def tool_advance(graph, node_id, obs_store):
    """Move forward in the decision graph."""
    step = get_step(graph, node_id)
    result = verify_expected(step.expected, obs_store)
    next_node = advance_state(step, result)
    return next_node, result