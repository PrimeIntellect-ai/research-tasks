# test_final_state.py
import os
import pytest

SCRIPT_PATH = "/home/user/analyze_audit.sh"
REPORT_PATH = "/home/user/compromise_report.csv"

def test_script_exists_and_executable():
    """Check if the bash script exists and is executable."""
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_report_content():
    """Check if the generated report matches the expected output."""
    assert os.path.exists(REPORT_PATH), f"Report file {REPORT_PATH} does not exist."

    with open(REPORT_PATH, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "Source_User,Target_Entity,Hops",
        "alice_admin,CustomerData,2",
        "charlie_ops,CustomerData,2",
        "charlie_ops,TempData,2",
        "alice_admin,LedgerMain,3"
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"Report content does not match expected output.\n"
        f"Expected:\n{expected_lines}\n"
        f"Actual:\n{actual_lines}"
    )