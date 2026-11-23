from collections.abc import Callable
from typing import Any
from svf_aa.core.schemas import AgentOutput, Decision, FrameworkResult
from svf_aa.core.framework import SVFAA


class RecoveryManager:
    """Retries a safe, caller-provided operation. Never automatically retries side effects."""
    def __init__(self, framework: SVFAA, max_retries: int = 2):
        if max_retries < 0:
            raise ValueError("max_retries must be >= 0")
        self.framework = framework
        self.max_retries = max_retries

    def run(self, make_output: Callable[[], AgentOutput], *, retry_safe: bool = False) -> tuple[FrameworkResult, int]:
        attempts = 0
        while True:
            attempts += 1
            result = self.framework.verify(make_output())
            if result.decision != Decision.RETRY_AGENT:
                return result, attempts
            if not retry_safe or attempts > self.max_retries:
                return result, attempts
