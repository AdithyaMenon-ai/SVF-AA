from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Decision(str, Enum):
    ACCEPT = "ACCEPT"
    ACCEPT_WITH_WARNINGS = "ACCEPT_WITH_WARNINGS"
    AUTO_CORRECT = "AUTO_CORRECT"
    RETRY_AGENT = "RETRY_AGENT"
    REPLAN_WORKFLOW = "REPLAN_WORKFLOW"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    ABORT = "ABORT"


@dataclass
class AgentOutput:
    agent_name: str
    input_data: Any
    output_data: Any
    context: dict[str, Any] = field(default_factory=dict)
    evidence: dict[str, Any] = field(default_factory=dict)
    constraints: dict[str, Any] = field(default_factory=dict)


@dataclass
class VerificationResult:
    verifier_name: str
    passed: bool
    score: float
    issues: list[str] = field(default_factory=list)
    severity: str = "none"
    applicable: bool = True


@dataclass
class FrameworkResult:
    agent_name: str
    decision: Decision
    confidence: float
    risk_score: float
    verification_results: list[VerificationResult]
    issues: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
