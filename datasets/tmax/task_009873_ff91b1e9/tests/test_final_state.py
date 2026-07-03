# test_final_state.py

import os
import subprocess
import pytest

def test_hook_exists_and_executable():
    """Verify the post-receive hook exists and is executable."""
    hook_path = "/home/user/targets.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Hook file does not exist at {hook_path}"
    assert os.access(hook_path, os.X_OK), f"Hook file at {hook_path} is not executable"

    with open(hook_path, "r") as f:
        first_line = f.readline().strip()
    assert "python" in first_line.lower(), f"Hook script does not appear to be a Python script. First line: {first_line}"

def test_alerts_log_exists():
    """Verify the alerts.log file exists."""
    log_path = "/home/user/alerts.log"
    assert os.path.isfile(log_path), f"Log file does not exist at {log_path}"

def test_alerts_log_contents():
    """Verify the alerts.log contains the correct alert and omits the successful connection."""
    log_path = "/home/user/alerts.log"
    with open(log_path, "r") as f:
        log_contents = f.read()

    expected_alert = "ALERT: Cannot connect to 127.0.0.1:10001"
    unexpected_alert = "ALERT: Cannot connect to 127.0.0.1:10000"

    assert expected_alert in log_contents, f"Expected alert '{expected_alert}' not found in {log_path}"
    assert unexpected_alert not in log_contents, f"Unexpected alert '{unexpected_alert}' found in {log_path}"

def test_repo_has_commit():
    """Verify the bare repository has received the commit with services.json."""
    repo_path = "/home/user/targets.git"

    # Check if there are any commits
    result = subprocess.run(
        ["git", "log", "--name-only"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to run git log in the bare repository. Make sure a commit was pushed."
    assert "services.json" in result.stdout, "services.json was not found in the commit history of the bare repository."