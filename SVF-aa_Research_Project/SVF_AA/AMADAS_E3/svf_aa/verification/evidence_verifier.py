from math import isclose
from svf_aa.core.schemas import AgentOutput, VerificationResult
from .base_verifier import BaseVerifier


class EvidenceVerifier(BaseVerifier):
    """Checks output claims against *independent* expected evidence.

    evidence={"expected": {"accuracy": 0.92}, "tolerance": 0.001}
    """
    def verify(self, agent: AgentOutput) -> VerificationResult:
        expected = agent.evidence.get("expected")
        if expected is None:
            return VerificationResult("evidence", False, 0.0,
                                      ["Independent evidence not supplied"], "medium", False)
        if not isinstance(expected, dict) or not isinstance(agent.output_data, dict):
            return VerificationResult("evidence", False, 0.0,
                                      ["Evidence and output must be mappings"], "high")
        tolerance = float(agent.evidence.get("tolerance", 1e-6))
        if tolerance < 0:
            return VerificationResult("evidence", False, 0.0, ["Negative tolerance"], "high")
        issues = []
        for key, value in expected.items():
            actual = agent.output_data.get(key)
            if isinstance(value, (int, float)) and not isinstance(value, bool) and isinstance(actual, (int, float)) and not isinstance(actual, bool):
                equal = isclose(float(actual), float(value), rel_tol=0, abs_tol=tolerance)
            else:
                equal = actual == value
            if not equal:
                issues.append(f"{key}: expected {value!r}, received {actual!r}")
        score = (len(expected) - len(issues)) / len(expected) if expected else 1.0
        return VerificationResult("evidence", not issues, score, issues,
                                  "high" if issues else "none")
