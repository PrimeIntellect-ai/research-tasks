# test_final_state.py

import os
import subprocess
import pytest

def test_process_metrics_exists_and_executable():
    """Verify that process_metrics.sh exists and is executable."""
    script_path = "/home/user/app/process_metrics.sh"
    assert os.path.isfile(script_path), f"Script missing: {script_path} was not created."
    assert os.access(script_path, os.X_OK), f"Script not executable: {script_path} lacks execute permissions."

def test_run_e2e_exists_and_executable():
    """Verify that run_e2e.sh exists and is executable."""
    script_path = "/home/user/app/run_e2e.sh"
    assert os.path.isfile(script_path), f"Script missing: {script_path} was not created."
    assert os.access(script_path, os.X_OK), f"Script not executable: {script_path} lacks execute permissions."

def test_expected_txt_is_patched():
    """Verify that expected.txt has been updated to the new format via the patch."""
    expected_path = "/home/user/app/tests/expected.txt"
    assert os.path.isfile(expected_path), f"File missing: {expected_path} does not exist."

    with open(expected_path, "r") as f:
        content = f.read().strip()

    assert "/home,3" in content, "expected.txt does not contain the new patched format (e.g., '/home,3')."
    assert "3 /home" not in content, "expected.txt still contains the old format (e.g., '3 /home'). Did you apply the patch?"

def test_run_e2e_succeeds():
    """Verify that run_e2e.sh runs successfully and exits with code 0."""
    script_path = "/home/user/app/run_e2e.sh"

    # Run the e2e script
    result = subprocess.run(
        [script_path], 
        capture_output=True, 
        text=True, 
        cwd="/home/user/app"
    )

    assert result.returncode == 0, (
        f"run_e2e.sh failed with exit code {result.returncode}.\n"
        f"Stdout: {result.stdout}\n"
        f"Stderr: {result.stderr}"
    )

def test_actual_matches_expected():
    """Verify that actual.txt exactly matches expected.txt after running the E2E script."""
    actual_path = "/home/user/app/tests/actual.txt"
    expected_path = "/home/user/app/tests/expected.txt"

    assert os.path.isfile(actual_path), f"File missing: {actual_path} was not generated."

    with open(actual_path, "r") as f:
        actual_content = f.read().strip()

    with open(expected_path, "r") as f:
        expected_content = f.read().strip()

    assert actual_content == expected_content, (
        "actual.txt does not match expected.txt.\n"
        f"Actual output:\n{actual_content}\n\n"
        f"Expected output:\n{expected_content}"
    )