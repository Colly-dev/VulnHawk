
"""
src/core/cvss.py

CVSS 3.1 base score calculation and severity classification.

⚠️ LEGAL DISCLAIMER ⚠️
This tool is for EDUCATIONAL and AUTHORIZED testing only.
Please ensure you have explicit permission before scanning any target.
The authors assume NO LIABILITY for misuse, damage, or legal consequences.
"""

import logging
from typing import Dict, Any
from cvss import CVSS3

logger = logging.getLogger(__name__)

class CVSSCalculator:
    """
    Calculates CVSS 3.1 scores and classifies severity.
    """
    def __init__(self):
        pass

    def calculate_base_score(self, vector_string: str) -> Dict[str, Any]:
        """
        Calculates the CVSS 3.1 base score and returns severity.
        Example vector string: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
        """
        try:
            c = CVSS3(vector_string)
            base_score = c.base_score
            severity = self._get_severity_from_score(base_score)
            return {"base_score": base_score, "severity": severity, "vector": vector_string}
        except Exception as e:
            logger.error(f"Error calculating CVSS score for vector {vector_string}: {e}")
            return {"base_score": 0.0, "severity": "None", "vector": vector_string}

    def _get_severity_from_score(self, score: float) -> str:
        """
        Determines the severity level based on the CVSS score.
        """
        if score == 0.0:
            return "None"
        elif 0.1 <= score <= 3.9:
            return "Low"
        elif 4.0 <= score <= 6.9:
            return "Medium"
        elif 7.0 <= score <= 8.9:
            return "High"
        elif 9.0 <= score <= 10.0:
            return "Critical"
        else:
            return "Unknown"

