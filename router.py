"""
Task Router
-----------
Detects product type, fault category, and risk level
from text + observations.
"""
import re

HIGH_RISK_KEYWORDS = {"radiation", "high-voltage", "disassembly"}

def classify_product_and_fault(text: str, obs: dict) -> dict:
    product = "CT-WS" if "ct" in text.lower() or "scanner" in text.lower() else "GENERIC"
    fault = obs.get("error_code") or _extract_code(text)
    module = "cooling" if "cool" in text.lower() else "general"
    risk = "medium" if any(k in text.lower() for k in HIGH_RISK_KEYWORDS) else "low"
    return {"product": product, "module": module, "fault_code": fault, "risk": risk}

def _extract_code(text: str):
    m = re.search(r"(E\d{2,3})", text.upper())
    return m.group(1) if m else None