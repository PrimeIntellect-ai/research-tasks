# test_final_state.py

import os
import subprocess
import re
import pytest

def get_default_gateway():
    """Helper to determine the actual default gateway."""
    try:
        result = subprocess.run(
            ["ip", "route"],
            capture_output=True,
            text=True,
            check=True
        )
        for line in result.stdout.splitlines():
            if line.startswith("default via"):
                parts = line.split()
                if len(parts) >= 3:
                    return parts[2]
    except Exception:
        pass
    return None

def test_routing_info_file():
    """Verify routing_info.txt exists and contains the correct default gateway."""
    file_path = "/home/user/workspace/routing_info.txt"
    assert os.path.isfile(file_path), f"File missing: {file_path}"

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_gw = get_default_gateway()
    assert expected_gw is not None, "Could not determine default gateway of the system to verify."
    assert content == expected_gw, f"routing_info.txt contains '{content}', expected '{expected_gw}'"

def test_pre_receive_hook():
    """Verify the pre-receive hook exists, is executable, and is a Python 3 script."""
    hook_path = "/home/user/central.git/hooks/pre-receive"
    assert os.path.isfile(hook_path), f"pre-receive hook missing: {hook_path}"
    assert os.access(hook_path, os.X_OK), f"pre-receive hook is not executable: {hook_path}"

    with open(hook_path, "r") as f:
        content = f.read()

    assert "python3" in content.splitlines()[0] or "python" in content.splitlines()[0], "pre-receive hook does not appear to be a Python script (check shebang)."
    assert "sys.stdin" in content or "input(" in content or "sys.stdin.read" in content, "pre-receive hook does not appear to read from standard input."

def test_expect_script():
    """Verify the Expect script exists and contains the required commands."""
    script_path = "/home/user/workspace/deploy.exp"
    assert os.path.isfile(script_path), f"Expect script missing: {script_path}"

    with open(script_path, "r") as f:
        content = f.read()

    assert "git push origin master" in content, "Expect script missing 'git push origin master' command."
    assert "Enter Deployment Pin:" in content, "Expect script missing prompt string 'Enter Deployment Pin:'."
    assert "8821" in content, "Expect script missing the pin '8821'."

def test_push_log():
    """Verify push.log exists and indicates a successful push."""
    log_path = "/home/user/push.log"
    assert os.path.isfile(log_path), f"Log file missing: {log_path}"

    with open(log_path, "r") as f:
        content = f.read()

    assert "Enter Deployment Pin:" in content, "push.log does not contain the pin prompt."
    assert "master -> master" in content or "Everything up-to-date" in content or "refs/heads/master" in content, "push.log does not indicate a successful git push."

def test_central_repo_updated():
    """Verify that the central repository has accepted the commit with routing_info.txt."""
    central_repo = "/home/user/central.git"

    # Check if routing_info.txt exists in the HEAD of the central bare repo
    result = subprocess.run(
        ["git", "ls-tree", "-r", "HEAD"],
        cwd=central_repo,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to inspect central repository HEAD."
    assert "routing_info.txt" in result.stdout, "routing_info.txt was not found in the central repository HEAD. The push may have failed or the file was not committed."