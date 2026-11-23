from abc import ABC, abstractmethod
from svf_aa.core.schemas import AgentOutput, VerificationResult


class BaseVerifier(ABC):
    @abstractmethod
    def verify(self, agent: AgentOutput) -> VerificationResult:
        raise NotImplementedError
