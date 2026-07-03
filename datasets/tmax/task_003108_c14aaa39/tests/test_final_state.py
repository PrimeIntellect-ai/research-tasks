# test_final_state.py

import os
import re

def test_script_exists():
    script_path = "/home/user/validate_pipeline.py"
    assert os.path.exists(script_path), f"The script {script_path} was not found."
    assert os.path.isfile(script_path), f"{script_path} is not a valid file."

def test_report_exists():
    report_path = "/home/user/report.txt"
    assert os.path.exists(report_path), f"The report file {report_path} was not found."
    assert os.path.isfile(report_path), f"{report_path} is not a valid file."

def test_report_content():
    report_path = "/home/user/report.txt"
    with open(report_path, "r") as f:
        content = f.read().strip()

    # The expected values are derived from the fixed random seed in the setup script.
    expected_trace = "0.6121"
    expected_corr = "0.9995"

    expected_line1 = f"Covariance Trace: {expected_trace}"
    expected_line2 = f"PC1 Correlation: {expected_corr}"

    assert expected_line1 in content, f"Expected '{expected_line1}' to be in {report_path}. Found:\n{content}"
    assert expected_line2 in content, f"Expected '{expected_line2}' to be in {report_path}. Found:\n{content}"

    # Ensure the format is exactly as requested
    lines = content.splitlines()
    assert len(lines) >= 2, f"Expected at least 2 lines in {report_path}, found {len(lines)}"
    assert lines[0].strip() == expected_line1, f"First line of report does not match exactly. Expected: '{expected_line1}', Got: '{lines[0].strip()}'"
    assert lines[1].strip() == expected_line2, f"Second line of report does not match exactly. Expected: '{expected_line2}', Got: '{lines[1].strip()}'"