"""
Guardrails
----------
Implements safety rules, escalation logic, and auditing hooks.
"""
from schemas import Step

def is_high_risk(step: Step) -> bool:
    return step.risk in ("medium", "high")

def should_escalate(global_risk: str, conf: float, result: str, step: Step) -> bool:
    """Escalate if safety or confidence thresholds breached."""
    if global_risk == "high" or step.risk == "high":
        return True
    if conf < 0.5 and result == "unknown":
        return True
    return False

def escalate(session: dict, reason: str) -> dict:
    """Generate escalation summary for handoff."""
    return {
        "status": "handoff",
        "reason": reason,
        "context": {
            "product": session.get("product"),
            "fault_code": session.get("fault_code"),
            "obs": session.get("obs"),
            "node": session.get("node"),
            "trace": session.get("retrieved_docs", [])
        }
    }