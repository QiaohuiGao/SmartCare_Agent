"""
Graph Engine
------------
Executes YAML-defined troubleshooting graphs.
"""
import yaml, re
from schemas import Step, Result

GRAPH_PATH = "data/troubleshooting_graph.yaml"

def load_graph(product: str, fault_code: str) -> dict:
    """Load matching product + fault graph."""
    graphs = yaml.safe_load(open(GRAPH_PATH))
    for g in graphs:
        if g["product"] == product and g["fault_code"] == fault_code:
            return g
    return None

def get_step(graph: dict, node_id: str) -> Step:
    """Return current step object."""
    node = graph["nodes"][node_id]
    return Step(
        step_id=node_id,
        instruction=node["instruction"],
        expected=node["expected"],
        next_if_pass=node.get("next_if_pass"),
        next_if_fail=node.get("next_if_fail"),
        risk=node.get("risk", "low")
    )

def verify_expected(expected: dict, obs: dict) -> Result:
    """Compare actual observations with expected values."""
    etype = expected["type"]
    key = expected["key"]
    val = obs.get(key)
    if val is None:
        return "unknown"
    if etype == "numeric":
        lo, hi = expected["range"]
        return "pass" if lo <= float(val) <= hi else "fail"
    if etype == "enum":
        return "pass" if val in expected["in"] else "fail"
    if etype == "regex":
        return "pass" if re.search(expected["pattern"], str(val)) else "fail"
    return "unknown"

def advance_state(step: Step, result: Result) -> str:
    """Decide next node or exit state."""
    if result == "pass":
        return step.next_if_pass
    if result == "fail":
        return step.next_if_fail
    return None