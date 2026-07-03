# test_final_state.py

import os
import subprocess
import pytest

def test_deploy_system_script_runs_successfully():
    """Ensure deploy_system.sh runs successfully with exit code 0."""
    script_path = "/home/user/deploy_system.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"deploy_system.sh failed with return code {result.returncode}.\nStderr: {result.stderr}"

def test_locks_created_correctly():
    """Ensure the correct lock files are created in /home/user/locks/."""
    lock_dir = "/home/user/locks"
    assert os.path.isdir(lock_dir), f"Directory {lock_dir} does not exist."

    expected_locks = {"api.lock", "db.lock", "web.lock"}
    actual_locks = {f for f in os.listdir(lock_dir) if f.endswith(".lock")}

    assert actual_locks == expected_locks, f"Expected locks {expected_locks}, but found {actual_locks}."

def test_diagnostics_log_contents():
    """Ensure diagnostics.log contains the correct sorted absolute paths."""
    log_path = "/home/user/diagnostics.log"
    assert os.path.isfile(log_path), f"Diagnostics log {log_path} does not exist."

    expected_lines = [
        "/home/user/locks/api.lock",
        "/home/user/locks/db.lock",
        "/home/user/locks/web.lock"
    ]

    with open(log_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Diagnostics log contents are incorrect.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )