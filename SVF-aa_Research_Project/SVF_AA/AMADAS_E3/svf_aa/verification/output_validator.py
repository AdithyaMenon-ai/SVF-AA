from svf_aa.core.schemas import AgentOutput, VerificationResult
from .base_verifier import BaseVerifier


class OutputValidator(BaseVerifier):
    def verify(self, agent: AgentOutput) -> VerificationResult:
        value = agent.output_data
        issues = []
        if value is None or (isinstance(value, (str, list, dict, tuple, set)) and not value):
            issues.append("Output is missing or empty")
        return VerificationResult("output", not issues, 0.0 if issues else 1.0,
                                  issues, "high" if issues else "none")
