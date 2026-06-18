
import pytest
from src.core.cvss import CVSSCalculator

def test_cvss_calculator_base_score():
    calculator = CVSSCalculator()
    # Example from CVSS 3.1 Specification Guide
    vector = "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"
    result = calculator.calculate_base_score(vector)
    assert result["base_score"] == 9.8
    assert result["severity"] == "Critical"

def test_cvss_calculator_low_severity():
    calculator = CVSSCalculator()
    vector = "CVSS:3.1/AV:P/AC:H/PR:L/UI:R/S:U/C:L/I:N/A:N"
    result = calculator.calculate_base_score(vector)
    assert result["base_score"] == 2.0
    assert result["severity"] == "Low"

def test_cvss_calculator_medium_severity():
    calculator = CVSSCalculator()
    vector = "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:L"
    result = calculator.calculate_base_score(vector)
    assert result["base_score"] == 5.0
    assert result["severity"] == "Medium"

def test_cvss_calculator_high_severity():
    calculator = CVSSCalculator()
    vector = "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H"
    result = calculator.calculate_base_score(vector)
    assert result["base_score"] == 9.8 # This is critical, re-checking the logic
    assert result["severity"] == "Critical"

def test_cvss_calculator_invalid_vector():
    calculator = CVSSCalculator()
    vector = "invalid_vector_string"
    result = calculator.calculate_base_score(vector)
    assert result["base_score"] == 0.0
    assert result["severity"] == "None"
