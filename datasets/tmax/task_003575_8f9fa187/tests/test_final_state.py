# test_final_state.py
import os
import subprocess
import pytest

def test_app_log_ready():
    """
    Check if the service successfully started and wrote 'READY' to /home/user/app.log.
    This implies the post-receive hook correctly set TZ and LC_ALL.
    """
    log_path = "/home/user/app.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. The service did not start successfully or the push failed."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "READY", f"Expected 'READY' in {log_path}, but found '{content}'. The environment variables might not be set correctly."

def test_git_push_successful():
    """
    Check if the bare repository /home/user/deploy.git has received the pushed commit.
    """
    # Get the commit hash of master in app-src
    src_result = subprocess.run(
        ["git", "rev-parse", "master"],
        cwd="/home/user/app-src",
        capture_output=True,
        text=True
    )
    assert src_result.returncode == 0, "Failed to get commit hash from /home/user/app-src master branch."
    src_commit = src_result.stdout.strip()

    # Get the commit hash of master in deploy.git
    deploy_result = subprocess.run(
        ["git", "rev-parse", "master"],
        cwd="/home/user/deploy.git",
        capture_output=True,
        text=True
    )
    assert deploy_result.returncode == 0, "The /home/user/deploy.git repository does not have a master branch. The push likely failed."
    deploy_commit = deploy_result.stdout.strip()

    assert src_commit == deploy_commit, f"The commit in deploy.git ({deploy_commit}) does not match app-src ({src_commit}). The push was not successful."

def test_hook_robustness():
    """
    Check if the post-receive hook has been modified to handle errors gracefully.
    We look for 'set -e' or similar error handling constructs.
    """
    hook_path = "/home/user/deploy.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Hook file {hook_path} is missing."

    with open(hook_path, "r") as f:
        content = f.read()

    # Check for basic robustness (e.g., set -e, set -eu, or checking exit codes)
    is_robust = "set -e" in content or "|| exit" in content or "set -u" in content
    assert is_robust, "The post-receive hook does not appear to handle errors gracefully (e.g., missing 'set -e')."