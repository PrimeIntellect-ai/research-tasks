# test_final_state.py

import os
import subprocess
import pytest

def test_analyze_script_exists_and_executable():
    script_path = "/home/user/analyze.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_analyze_script_execution_and_output():
    script_path = "/home/user/analyze.sh"
    report_path = "/home/user/report.txt"

    # Remove the report if it already exists to ensure we are testing the script's output
    if os.path.exists(report_path):
        os.remove(report_path)

    # Run the script
    try:
        result = subprocess.run([script_path], capture_output=True, text=True, timeout=10)
    except subprocess.TimeoutExpired:
        pytest.fail(f"Script {script_path} timed out during execution.")

    assert result.returncode == 0, f"Script failed with return code {result.returncode}.\nStderr: {result.stderr}"

    assert os.path.isfile(report_path), f"Report file {report_path} was not created by the script."

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "COMPROMISED_FILE: app.js",
        "ROGUE_ISSUER: EvilRogueCA-999",
        "ATTACKER_IP: 203.0.113.8"
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in report, got {len(actual_lines)}.\nContent:\n{content}"

    for expected, actual in zip(expected_lines, actual_lines):
        assert actual == expected, f"Mismatch in report. Expected: '{expected}', Got: '{actual}'"