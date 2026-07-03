# test_final_state.py

import os
import subprocess
import pytest

def test_resolution_log_exists_and_correct():
    log_path = "/home/user/resolution.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert "SYSTEM_RESTORED_SUCCESS" in content, (
        f"Log file {log_path} does not contain the required success message. "
        f"Found: '{content}'"
    )

def test_telemd_compiled_binary_exists():
    binary_path = "/home/user/telemd/telemd"
    assert os.path.isfile(binary_path), (
        f"Compiled binary {binary_path} does not exist. "
        "Make sure you recompiled the service using 'make'."
    )
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_telemd_test_script_passes():
    script_path = "/home/user/telemd/test_telemd.sh"
    assert os.path.isfile(script_path), f"Test script {script_path} is missing."

    # Run the test script to ensure the service no longer crashes
    result = subprocess.run(
        [script_path],
        cwd="/home/user/telemd",
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, (
        f"Test script {script_path} failed with exit code {result.returncode}. "
        f"The service might still be crashing. Output: {result.stdout.strip()} {result.stderr.strip()}"
    )