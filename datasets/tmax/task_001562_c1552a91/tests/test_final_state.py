# test_final_state.py

import os
import pytest

REPORT_PATH = "/home/user/incident_report.txt"
RECOVERY_EXEC = "/home/user/data_processor/recovery"

EXPECTED_REPORT_CONTENT = """SECRET_KEY: x9F2kL_pQ8zV1
LAST_TXN_ID: 7734190
DEADLOCK_HASH: A8F93B2C9E1045F1"""

def test_recovery_executable_built():
    assert os.path.isfile(RECOVERY_EXEC), "The 'recovery' executable was not built."
    assert os.access(RECOVERY_EXEC, os.X_OK), "The 'recovery' file is not executable."

def test_incident_report_exists():
    assert os.path.isfile(REPORT_PATH), f"Incident report not found at {REPORT_PATH}."

def test_incident_report_content():
    assert os.path.isfile(REPORT_PATH), f"Incident report not found at {REPORT_PATH}."
    with open(REPORT_PATH, "r") as f:
        content = f.read().strip()

    # Check each line to provide better error messages
    expected_lines = EXPECTED_REPORT_CONTENT.splitlines()
    actual_lines = content.splitlines()

    assert len(actual_lines) >= 3, "Incident report does not have enough lines."

    assert actual_lines[0].strip() == expected_lines[0], f"Expected first line to be '{expected_lines[0]}', but got '{actual_lines[0]}'."
    assert actual_lines[1].strip() == expected_lines[1], f"Expected second line to be '{expected_lines[1]}', but got '{actual_lines[1]}'."
    assert actual_lines[2].strip() == expected_lines[2], f"Expected third line to be '{expected_lines[2]}', but got '{actual_lines[2]}'."