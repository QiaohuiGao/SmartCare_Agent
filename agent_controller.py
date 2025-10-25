"""
Agent Controller
----------------
Coordinates each user interaction cycle:
1. Normalize multimodal input.
2. Route task & classify product/fault.
3. Retrieve relevant knowledge.
4. Execute reasoning & graph traversal.
5. Verify results & apply guardrails.
6. Produce safe, structured output.
"""
from multimodal_parser import asr_to_text, ocr_image, vision_hint
from router import classify_product_and_fault
from retriever import retrieve_kb
from graph_engine import load_graph, get_step, verify_expected, advance_state
from guardrails import should_escalate, escalate

def handle_turn(turn, session: dict) -> dict:
    """Main reasoning loop per user turn."""
    text, new_obs = "", {}
    # --- Input Fusion Layer ---
    if turn.mode == "text":
        text = turn.payload
    elif turn.mode == "audio":
        text = asr_to_text(turn.payload)
    elif turn.mode == "image":
        new_obs = ocr_image(turn.payload)
        vision_obs = vision_hint(turn.payload)
        new_obs.update(vision_obs)
        text = f"Image evidence: {new_obs}"
    session.setdefault("obs", {}).update(new_obs)

    # --- Task Router ---
    route = classify_product_and_fault(text, session["obs"])
    session.update(route)

    # --- Hybrid Retrieval ---
    docs = retrieve_kb(text, filters=route)
    session["retrieved_docs"] = [d["id"] for d in docs]

    # --- Troubleshooting Graph Engine ---
    graph = load_graph(session["product"], session.get("fault_code"))
    if not graph:
        return escalate(session, "graph_not_found")

    node = session.get("node") or graph["start"]
    step = get_step(graph, node)
    result = verify_expected(step.expected, session["obs"])
    next_node = advance_state(step, result)
    session["node"] = next_node or node

    # --- Confidence & Guardrails ---
    if should_escalate(route["risk"], 0.8, result, step):
        return escalate(session, "safety_triggered")

    # --- Structured Output ---
    if next_node == "EXIT_SUCCESS":
        return {
            "status": "resolved",
            "summary": f"Resolved at {node} ({result})",
            "trace": session.get("retrieved_docs", [])
        }

    return {
        "status": "in_progress",
        "current_step": step.step_id,
        "instruction": step.instruction,
        "expected": step.expected,
        "next_node": next_node,
        "confidence": 0.8
    }