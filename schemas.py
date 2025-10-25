"""
Schemas
-------
Lightweight data structures used throughout SmartCare-Agent.
"""
from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional

Mode = Literal["text", "image", "audio"]
Result = Literal["pass", "fail", "unknown"]

@dataclass
class Turn:
    mode: Mode
    payload: Any

@dataclass
class Observation:
    key: str
    value: Any
    confidence: float = 1.0

@dataclass
class Step:
    step_id: str
    instruction: str
    expected: Dict[str, Any]
    next_if_pass: Optional[str]
    next_if_fail: Optional[str]
    risk: Literal["low", "medium", "high"] = "low"

@dataclass
class StepResult:
    instruction: str
    checks: List[str]
    next_state: Optional[str]
    risk: str