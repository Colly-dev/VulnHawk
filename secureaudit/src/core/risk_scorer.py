
from typing import List, Dict, Any

class RiskScorer:
    SEVERITY_WEIGHTS = {
        "CRITICAL": 10,
        "HIGH": 7,
        "MEDIUM": 4,
        "LOW": 1,
        "INFO": 0
    }

    @staticmethod
    def calculate_score(findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates the overall security score based on findings.
        A score of 100 is perfect, 0 is worst.
        """
        if not findings:
            return {"score": 100, "rating": "Excellent", "total_findings": 0}

        total_weight = 0
        severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}

        for finding in findings:
            severity = finding.get("severity", "INFO").upper()
            weight = RiskScorer.SEVERITY_WEIGHTS.get(severity, 0)
            total_weight += weight
            severity_counts[severity] += 1

        # Simple scoring algorithm: 
        # Start with 100, subtract weighted penalty. 
        # Cap at 0.
        penalty_factor = 2  # Adjust this to tune the score sensitivity
        score = max(0, 100 - (total_weight * penalty_factor))
        
        rating = RiskScorer._get_rating(score)

        return {
            "score": round(score, 2),
            "rating": rating,
            "total_findings": len(findings),
            "severity_counts": severity_counts
        }

    @staticmethod
    def _get_rating(score: float) -> str:
        if score >= 90: return "Excellent"
        if score >= 75: return "Good"
        if score >= 60: return "Fair"
        if score >= 40: return "Poor"
        return "Critical"
