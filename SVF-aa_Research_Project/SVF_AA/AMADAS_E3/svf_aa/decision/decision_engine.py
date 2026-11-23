from svf_aa.core.schemas import Decision, VerificationResult


class DecisionEngine:
    def decide(self, results: list[VerificationResult], risk: float) -> Decision:
        if not results:
            return Decision.HUMAN_REVIEW
        if any(r.severity == "high" and not r.passed for r in results if r.applicable):
            return Decision.RETRY_AGENT
        if any(not r.applicable for r in results):
            return Decision.HUMAN_REVIEW
        if any(not r.passed for r in results):
            return Decision.ACCEPT_WITH_WARNINGS if risk < 0.3 else Decision.HUMAN_REVIEW
        return Decision.ACCEPT
