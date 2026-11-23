from collections.abc import Callable
from typing import Any
from svf_aa.core.framework import SVFAA
from svf_aa.core.schemas import AgentOutput, Decision, FrameworkResult


class VerificationRejected(RuntimeError):
    def __init__(self, result: FrameworkResult):
        self.result = result
        super().__init__(f"Verification rejected {result.agent_name}: {result.decision.value}")


class LangGraphAdapter:
    """Wraps a LangGraph node for E3; do NOT use in E1 baseline."""
    def __init__(self, framework: SVFAA):
        self.framework = framework

    def wrap(self, name: str, node: Callable[[dict[str, Any]], dict[str, Any]],
             evidence_factory: Callable[[dict, dict], dict] | None = None,
             constraints: dict | None = None) -> Callable:
        def verified_node(state: dict[str, Any]) -> dict[str, Any]:
            update = node(state)
            evidence = evidence_factory(state, update) if evidence_factory else {}
            result = self.framework.verify(AgentOutput(
                agent_name=name, input_data=state, output_data=update,
                evidence=evidence, constraints=constraints or {}
            ))
            if result.decision not in (Decision.ACCEPT, Decision.ACCEPT_WITH_WARNINGS):
                raise VerificationRejected(result)
            return update
        return verified_node
