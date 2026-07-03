# test_final_state.py

import os
import pytest

SCRIPT_PATH = "/home/user/find_cycles.sh"
REPORT_PATH = "/home/user/deadlock_report.log"

def test_script_exists_and_executable():
    """Check if the find_cycles.sh script exists and is executable."""
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable"

def test_report_exists():
    """Check if the deadlock_report.log file was generated."""
    assert os.path.exists(REPORT_PATH), f"Report file not found at {REPORT_PATH}"
    assert os.path.isfile(REPORT_PATH), f"{REPORT_PATH} is not a file"

def test_report_content():
    """Check if the deadlock_report.log contains the correct length-3 cycles."""
    expected_lines = [
        "auditor-billing-compliance",
        "dev-qa-staging"
    ]

    with open(REPORT_PATH, "r") as f:
        content = f.read().strip()

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"Report content does not match expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )