# test_final_state.py

import os
import pytest

REPORT_PATH = '/home/user/forensics_report.txt'

def test_forensics_report_exists():
    assert os.path.isfile(REPORT_PATH), f"The report file {REPORT_PATH} is missing. Ensure you created it in the correct location."

def test_forensics_report_content():
    with open(REPORT_PATH, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 3, f"The report file should contain exactly 3 lines, but found {len(lines)}."

    expected_line1 = "sysstat"
    expected_line2 = "A9f8B1c03dE"
    expected_line3 = "7492"

    assert lines[0] == expected_line1, f"Line 1 is incorrect. Expected the tampered binary name '{expected_line1}', but got '{lines[0]}'."
    assert lines[1] == expected_line2, f"Line 2 is incorrect. Expected the session_id '{expected_line2}', but got '{lines[1]}'."
    assert lines[2] == expected_line3, f"Line 3 is incorrect. Expected the cracked PIN '{expected_line3}', but got '{lines[2]}'."