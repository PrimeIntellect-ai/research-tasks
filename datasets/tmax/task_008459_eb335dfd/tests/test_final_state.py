# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/audit_graph.sh"
REPORT_PATH = "/home/user/compliance_report.txt"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"Path {SCRIPT_PATH} is not a file."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_script_execution_and_output():
    # Remove the report if it exists from a previous run to ensure the script creates it
    if os.path.exists(REPORT_PATH):
        os.remove(REPORT_PATH)

    # Execute the script
    try:
        result = subprocess.run(
            [SCRIPT_PATH],
            cwd="/home/user",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=15
        )
        assert result.returncode == 0, f"Script failed with return code {result.returncode}.\nStderr: {result.stderr}"
    except Exception as e:
        pytest.fail(f"Failed to execute script: {e}")

    # Check that the report was created
    assert os.path.exists(REPORT_PATH), f"Report file {REPORT_PATH} was not created by the script."

    # Read and verify the report content
    with open(REPORT_PATH, "r") as f:
        content = f.read().strip()

    expected_content = (
        "CYCLES:\n"
        "ACC_010,ACC_011,ACC_012\n"
        "EXPOSURE_DISTANCE:\n"
        "3"
    )

    assert content == expected_content, (
        f"Report content does not match expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Got:\n{content}"
    )