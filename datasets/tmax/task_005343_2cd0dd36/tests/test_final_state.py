# test_final_state.py
import os
import subprocess
import re

def test_supervisor_script_exists_and_executable():
    script_path = "/home/user/supervisor.py"
    assert os.path.exists(script_path), f"Missing {script_path}"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"

def test_cron_file_exists_and_correct():
    cron_path = "/home/user/restore_cron"
    assert os.path.exists(cron_path), f"Missing {cron_path}"

    with open(cron_path, "r") as f:
        content = f.read().strip()

    # Allow some flexibility with spaces, but exact command
    match = re.search(r"^\*\s+\*\s+\*\s+\*\s+\*\s+/usr/bin/env\s+python3\s+/home/user/supervisor\.py$", content, re.MULTILINE)
    assert match, f"Cron file {cron_path} does not contain the correct schedule and command. Found: {content}"

def test_supervisor_behavior_success():
    log_path = "/home/user/supervisor.log"
    state_path = "/home/user/.restore_state"

    # Clean up before run
    if os.path.exists(log_path):
        os.remove(log_path)
    if os.path.exists(state_path):
        os.remove(state_path)

    # Run the supervisor
    result = subprocess.run(["/usr/bin/env", "python3", "/home/user/supervisor.py"], capture_output=True)
    assert result.returncode == 0, f"Supervisor script should exit with 0 on success, got {result.returncode}"

    assert os.path.exists(log_path), f"Log file {log_path} was not created"

    with open(log_path, "r") as f:
        log_content = f.read().strip().split('\n')

    expected_log = [
        "[RETRY] Restore failed, attempt 1 of 4",
        "[RETRY] Restore failed, attempt 2 of 4",
        "[SUCCESS] Restore completed"
    ]

    assert log_content == expected_log, f"Log content does not match expected output. Got: {log_content}"

def test_supervisor_behavior_fatal():
    log_path = "/home/user/supervisor.log"
    script_path = "/home/user/run_restore.sh"

    # Clean up before run
    if os.path.exists(log_path):
        os.remove(log_path)

    # Backup original script
    with open(script_path, "r") as f:
        original_script = f.read()

    try:
        # Create a script that always fails
        with open(script_path, "w") as f:
            f.write("#!/bin/bash\nexit 1\n")

        # Run the supervisor
        result = subprocess.run(["/usr/bin/env", "python3", "/home/user/supervisor.py"], capture_output=True)
        assert result.returncode != 0, "Supervisor script should exit with non-zero code when max retries reached"

        assert os.path.exists(log_path), f"Log file {log_path} was not created"

        with open(log_path, "r") as f:
            log_content = f.read().strip().split('\n')

        assert len(log_content) == 5, f"Expected 5 log lines (4 retries + 1 fatal), got {len(log_content)}"
        assert log_content[-1] == "[FATAL] Restore failed after 4 attempts", f"Expected fatal message, got: {log_content[-1]}"

        for i in range(1, 5):
            assert log_content[i-1] == f"[RETRY] Restore failed, attempt {i} of 4", f"Expected retry line {i}, got: {log_content[i-1]}"

    finally:
        # Restore original script
        with open(script_path, "w") as f:
            f.write(original_script)