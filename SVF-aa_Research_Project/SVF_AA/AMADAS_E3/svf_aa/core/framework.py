from svf_aa.core.schemas import AgentOutput, FrameworkResult
from svf_aa.verification.output_validator import OutputValidator
from svf_aa.verification.evidence_verifier import EvidenceVerifier
from svf_aa.verification.constraint_verifier import ConstraintVerifier
from svf_aa.verification.reasoning_verifier import ReasoningVerifier
from svf_aa.decision.risk_assessor import RiskAssessor
from svf_aa.decision.decision_engine import DecisionEngine
from svf_aa.monitoring.verification_logger import VerificationLogger


class SVFAA:
    def __init__(self, verifiers=None, log_dir="outputs/verification_logs"):
        self.verifiers = verifiers if verifiers is not None else [
            OutputValidator(), EvidenceVerifier(), ConstraintVerifier(), ReasoningVerifier()
        ]
        self.risk_assessor = RiskAssessor()
        self.decision_engine = DecisionEngine()
        self.logger = VerificationLogger(log_dir)

    def verify(self, agent: AgentOutput, *, log=True) -> FrameworkResult:
        results = [verifier.verify(agent) for verifier in self.verifiers]
        confidence, risk = self.risk_assessor.assess(results)
        decision = self.decision_engine.decide(results, risk)
        outcome = FrameworkResult(
            agent_name=agent.agent_name,
            decision=decision,
            confidence=confidence,
            risk_score=risk,
            verification_results=results,
            issues=[issue for result in results for issue in result.issues],
            metadata={"applicable_verifiers": sum(r.applicable for r in results),
                      "total_verifiers": len(results)},
        )
        if log:
            outcome.metadata["log_path"] = self.logger.log(outcome)
        return outcome
