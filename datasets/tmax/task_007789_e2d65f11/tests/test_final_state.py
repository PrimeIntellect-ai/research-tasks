# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/audit_path.sh"
RESULTS_PATH = "/home/user/audit_results.txt"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_audit_results_content():
    assert os.path.isfile(RESULTS_PATH), f"Results file {RESULTS_PATH} does not exist."

    with open(RESULTS_PATH, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, f"Expected at least 2 lines in {RESULTS_PATH}, found {len(lines)}."

    expected_line_1 = "Employee:Mallory -> Group:Interns -> Group:Dev_Team -> Group:Engineering -> Group:SuperAdmins -> Resource:Project_Apollo_Secrets"
    expected_line_2 = "NO_ACCESS"

    assert lines[0] == expected_line_1, f"Line 1 in {RESULTS_PATH} is incorrect. Expected: '{expected_line_1}', Got: '{lines[0]}'"
    assert lines[1] == expected_line_2, f"Line 2 in {RESULTS_PATH} is incorrect. Expected: '{expected_line_2}', Got: '{lines[1]}'"

def test_script_dynamic_execution():
    # Test a scenario not explicitly required in the output file to ensure dynamic querying works
    try:
        result = subprocess.run(
            [SCRIPT_PATH, "Bob", "Financial_Q4_Report"],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        expected_output = "Employee:Bob -> Group:HR -> Group:All_Staff -> Resource:Financial_Q4_Report"
        assert output == expected_output, f"Script failed dynamic test. Expected: '{expected_output}', Got: '{output}'"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script execution failed: {e.stderr}")

def test_script_dynamic_execution_no_access():
    # Test a user with no access
    try:
        result = subprocess.run(
            [SCRIPT_PATH, "Alice", "Project_Apollo_Secrets"],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        expected_output = "NO_ACCESS"
        assert output == expected_output, f"Script failed dynamic NO_ACCESS test. Expected: '{expected_output}', Got: '{output}'"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script execution failed: {e.stderr}")