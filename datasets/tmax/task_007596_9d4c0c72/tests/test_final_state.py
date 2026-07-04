# test_final_state.py

import os
import re
import pytest

def test_report_exists():
    report_path = "/home/user/ticket8022/report.txt"
    assert os.path.isfile(report_path), f"The report file {report_path} is missing."

def test_report_contents():
    report_path = "/home/user/ticket8022/report.txt"
    assert os.path.isfile(report_path), f"The report file {report_path} is missing."

    with open(report_path, "r") as f:
        content = f.read()

    # Extract values using regex to allow minor formatting variations
    lr_match = re.search(r"LEARNING_RATE:\s*([0-9.]+)", content)
    dp_match = re.search(r"DATA_POINTS:\s*([0-9]+)", content)
    cv_match = re.search(r"CONVERGED_VALUE:\s*([0-9.]+)", content)

    assert lr_match is not None, "LEARNING_RATE not found in report.txt in the expected format."
    assert dp_match is not None, "DATA_POINTS not found in report.txt in the expected format."
    assert cv_match is not None, "CONVERGED_VALUE not found in report.txt in the expected format."

    learning_rate = float(lr_match.group(1))
    data_points = int(dp_match.group(1))
    converged_value = float(cv_match.group(1))

    assert abs(learning_rate - 0.05) < 1e-6, f"Expected LEARNING_RATE to be 0.05, got {learning_rate}"
    assert data_points == 5, f"Expected DATA_POINTS to be 5, got {data_points}"
    assert abs(converged_value - 3.7550) < 1e-4, f"Expected CONVERGED_VALUE to be approximately 3.7550, got {converged_value}"