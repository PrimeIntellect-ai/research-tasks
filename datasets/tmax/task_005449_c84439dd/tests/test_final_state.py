# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/collect_diagnostics.sh"
REPORT_PATH = "/home/user/diagnostics_report.txt"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_script_execution_and_report_generation():
    # Remove the report if it exists from previous manual runs
    if os.path.exists(REPORT_PATH):
        os.remove(REPORT_PATH)

    # Run the script
    result = subprocess.run([SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Script executed with non-zero exit code {result.returncode}.\nStderr: {result.stderr}"

    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} was not created by the script."

def test_report_content():
    # Ensure the script is run if tests are executed out of order, though pytest usually runs top-down
    if not os.path.exists(REPORT_PATH):
        subprocess.run([SCRIPT_PATH], capture_output=True, text=True)

    with open(REPORT_PATH, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "CONFLICTING_PACKAGE=numpy",
        "REQUIRED_VERSION=1.23.5",
        "INSTALLED_VERSION=1.24.2",
        "FIRST_FATAL_TIMESTAMP=2023-10-25T10:01:02Z"
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"Report content does not match expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )