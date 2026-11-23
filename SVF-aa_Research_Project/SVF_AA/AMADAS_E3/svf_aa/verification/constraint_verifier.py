from svf_aa.core.schemas import AgentOutput, VerificationResult
from .base_verifier import BaseVerifier


class ConstraintVerifier(BaseVerifier):
    """Supported constraints: required_keys, numeric_ranges, allowed_values."""
    def verify(self, agent: AgentOutput) -> VerificationResult:
        rules = agent.constraints
        if not rules:
            return VerificationResult("constraints", False, 0.0,
                                      ["No constraints provided"], "low", False)
        output = agent.output_data
        if not isinstance(output, dict):
            return VerificationResult("constraints", False, 0.0,
                                      ["Constraints require dictionary output"], "high")
        issues = []
        checks = 0
        for key in rules.get("required_keys", []):
            checks += 1
            if key not in output:
                issues.append(f"Missing required key: {key}")
        for key, bounds in rules.get("numeric_ranges", {}).items():
            checks += 1
            value = output.get(key)
            if not isinstance(value, (int, float)) or isinstance(value, bool) or not bounds[0] <= value <= bounds[1]:
                issues.append(f"{key} must be between {bounds[0]} and {bounds[1]}")
        for key, allowed in rules.get("allowed_values", {}).items():
            checks += 1
            if output.get(key) not in allowed:
                issues.append(f"{key} is not an allowed value")
        if not checks:
            return VerificationResult("constraints", False, 0.0,
                                      ["No supported constraint checks"], "low", False)
        return VerificationResult("constraints", not issues,
                                  (checks - len(issues)) / checks, issues,
                                  "high" if issues else "none")
