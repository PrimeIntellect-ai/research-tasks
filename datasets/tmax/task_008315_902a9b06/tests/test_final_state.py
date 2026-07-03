# test_final_state.py

import os
import pytest

def test_processed_data_exists():
    """Check if the processed_data.csv file exists."""
    file_path = "/home/user/processed_data.csv"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. The Go program must create it."

def test_processed_data_content():
    """Check if the processed_data.csv file has the exact expected content."""
    file_path = "/home/user/processed_data.csv"

    expected_content = """PatientID,Age,Condition,BiomarkerA,BiomarkerB,RiskScore
1,45,Healthy,2.50,1.20,93.75
2,60,AtRisk,3.10,0.50,372.00
3,30,Healthy,1.80,2.00,27.00
4,75,Critical,4.50,0.00,0.00"""

    with open(file_path, "r") as f:
        content = f.read().strip()

    # Normalize line endings for comparison
    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"Content of {file_path} is incorrect.\n"
        f"Expected:\n{expected_content}\n"
        f"Actual:\n{content}"
    )