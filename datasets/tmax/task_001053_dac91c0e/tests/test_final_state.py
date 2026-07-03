# test_final_state.py

import os
import re
import pytest

def test_compute_lu_script_exists():
    """Check if the bash script compute_lu.sh exists."""
    script_path = "/home/user/compute_lu.sh"
    assert os.path.isfile(script_path), f"Script not found: {script_path}"

def test_report_exists():
    """Check if the report.txt exists."""
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"Report file not found: {report_path}"

def test_report_content():
    """Validate the content and format of report.txt."""
    report_path = "/home/user/report.txt"
    if not os.path.exists(report_path):
        pytest.fail(f"Report file missing: {report_path}")

    with open(report_path, "r") as f:
        content = f.read()

    # Check Execution Time
    time_match = re.search(r"Execution Time:\s*([0-9]*\.?[0-9]+)\s*seconds", content)
    assert time_match is not None, "Report missing or invalid 'Execution Time: <time> seconds' format."

    # Check Max Error
    error_match = re.search(r"Max Error:\s*([0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?)", content)
    assert error_match is not None, "Report missing or invalid 'Max Error: <error_value>' format."

    error_val = float(error_match.group(1))
    assert error_val < 1e-5, f"Max Error is not strictly less than 1e-5. Found: {error_val}"

    # Check Test Outcome
    test_match = re.search(r"Test:\s*(PASS|FAIL)", content)
    assert test_match is not None, "Report missing or invalid 'Test: PASS' format."
    assert test_match.group(1) == "PASS", f"Expected Test: PASS, but found Test: {test_match.group(1)}"