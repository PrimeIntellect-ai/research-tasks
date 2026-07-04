# test_final_state.py

import os
import re
import pytest

def test_report_exists():
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"Expected report file {report_path} was not found."

def test_report_content():
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"Expected report file {report_path} was not found."

    with open(report_path, "r") as f:
        content = f.read()

    # Check TX99 score (4.28 or 4.29)
    assert re.search(r"TX99:4\.2[89]", content), "TX99 score is missing or incorrect in report.txt. Expected 4.28 or 4.29."

    # Check TZ88 score (8.14 or 8.15)
    assert re.search(r"TZ88:8\.1[45]", content), "TZ88 score is missing or incorrect in report.txt. Expected 8.14 or 8.15."

    # Check QW12 score (2.25)
    assert re.search(r"QW12:2\.25", content), "QW12 score is missing or incorrect in report.txt. Expected 2.25."