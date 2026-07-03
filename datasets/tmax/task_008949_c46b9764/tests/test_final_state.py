# test_final_state.py

import os
import pytest

def test_report_exists():
    report_path = "/home/user/report.txt"
    assert os.path.exists(report_path), f"The file {report_path} does not exist. Your script did not generate the report."
    assert os.path.isfile(report_path), f"The path {report_path} is not a file."

def test_report_content():
    report_path = "/home/user/report.txt"
    expected_content = """Log Analysis Report
===================
Start Time: 2023-10-01 10:00:00
End Time: 2023-10-01 11:45:00
Total Resampled Intervals: 8
Max Value (after gap-filling): 56.00"""

    if not os.path.exists(report_path):
        pytest.fail(f"Cannot check content because {report_path} does not exist.")

    with open(report_path, 'r') as f:
        content = f.read().strip()

    assert content == expected_content, f"The content of {report_path} does not match the expected template and values. Found:\n{content}"