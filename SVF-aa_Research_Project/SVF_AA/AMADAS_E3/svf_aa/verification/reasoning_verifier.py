from math import isclose
from svf_aa.core.schemas import AgentOutput, VerificationResult
from .base_verifier import BaseVerifier


class ReasoningVerifier(BaseVerifier):
    """Checks explicit arithmetic steps, NOT arbitrary natural-language reasoning.

    context['calculations'] = [{'operation':'add','a':2,'b':3,'result':5}]
    """
    def verify(self, agent: AgentOutput) -> VerificationResult:
        steps = agent.context.get("calculations")
        if not steps:
            return VerificationResult("reasoning", False, 0.0,
                                      ["No verifiable calculation steps provided"], "low", False)
        issues = []
        operations = {"add": lambda a,b: a+b, "subtract": lambda a,b: a-b,
                      "multiply": lambda a,b: a*b, "divide": lambda a,b: a/b}
        for i, step in enumerate(steps):
            try:
                fn = operations[step["operation"]]
                a, b, actual = float(step["a"]), float(step["b"]), float(step["result"])
                expected = fn(a, b)
                if not isclose(expected, actual, rel_tol=1e-9, abs_tol=1e-9):
                    issues.append(f"Calculation step {i} incorrect")
            except (KeyError, ValueError, TypeError, ZeroDivisionError, OverflowError):
                issues.append(f"Calculation step {i} malformed or unsupported")
        return VerificationResult("reasoning", not issues,
                                  (len(steps)-len(issues))/len(steps), issues,
                                  "high" if issues else "none")
