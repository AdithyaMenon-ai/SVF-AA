from svf_aa.core.schemas import VerificationResult


class RiskAssessor:
    def assess(self, results: list[VerificationResult]) -> tuple[float, float]:
        applicable = [r for r in results if r.applicable]
        if not applicable:
            return 0.0, 1.0
        confidence = sum(max(0.0, min(1.0, r.score)) for r in applicable) / len(applicable)
        # Conservative penalty for missing verification coverage.
        coverage = len(applicable) / len(results) if results else 0.0
        confidence *= coverage
        return round(confidence, 4), round(1.0 - confidence, 4)
