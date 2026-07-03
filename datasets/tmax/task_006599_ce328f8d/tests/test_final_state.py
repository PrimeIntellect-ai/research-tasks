# test_final_state.py

import os
import subprocess
import pytest

def test_policy_audit_script_exists_and_executable():
    script_path = "/home/user/policy_audit.sh"
    assert os.path.isfile(script_path), f"Script missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_audit_results():
    script_path = "/home/user/policy_audit.sh"
    results_path = "/home/user/audit_results.txt"

    # Run the student's script
    try:
        result = subprocess.run([script_path], capture_output=True, text=True, timeout=10)
        assert result.returncode == 0, f"Script failed with return code {result.returncode}. Stderr: {result.stderr}"
    except Exception as e:
        pytest.fail(f"Failed to execute {script_path}: {e}")

    assert os.path.isfile(results_path), f"Output file missing: {results_path}"

    with open(results_path, "r") as f:
        actual_output = f.read().strip()

    expected_output = (
        "OPEN_REDIRECT_IPS: 172.16.0.4,192.168.1.100\n"
        "PRIVESC_VULN_FILES: backup.sh,stop.sh\n"
        "UNAUTHORIZED_PORTS: 22,3306,8080"
    )

    # Compare line by line to give better error messages
    actual_lines = [line.strip() for line in actual_output.splitlines() if line.strip()]
    expected_lines = expected_output.splitlines()

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {results_path}, got {len(actual_lines)}."

    for expected, actual in zip(expected_lines, actual_lines):
        assert expected == actual, f"Mismatch in {results_path}. Expected: '{expected}', Got: '{actual}'"