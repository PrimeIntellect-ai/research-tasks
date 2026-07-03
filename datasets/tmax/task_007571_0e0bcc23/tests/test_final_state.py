# test_final_state.py

import os
import re
import subprocess
import pytest

def test_fstab_simulation():
    fstab_path = "/home/user/my_fstab"
    assert os.path.exists(fstab_path), f"File {fstab_path} does not exist."

    with open(fstab_path, "r") as f:
        content = f.read()

    # Check for the correct mount configuration
    pattern = r"^/home/user/remote_share\s+/home/user/mnt/backup\s+nfs\s+defaults,ro"
    match = re.search(pattern, content, re.MULTILINE)
    assert match is not None, f"The fstab file does not contain the correct mount configuration. Found: {content}"

def test_directories_exist():
    remote_share = "/home/user/remote_share"
    mnt_backup = "/home/user/mnt/backup"

    assert os.path.isdir(remote_share), f"Directory {remote_share} does not exist."
    assert os.path.isdir(mnt_backup), f"Directory {mnt_backup} does not exist."

def test_git_bare_repo():
    repo_path = "/home/user/monitor.git"
    assert os.path.isdir(repo_path), f"Directory {repo_path} does not exist."

    # Check if it is a bare repository
    result = subprocess.run(
        ["git", "-C", repo_path, "rev-parse", "--is-bare-repository"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, "Git command failed on the bare repository."
    assert result.stdout.strip() == "true", f"The repository at {repo_path} is not a bare repository."

def test_git_post_receive_hook():
    hook_path = "/home/user/monitor.git/hooks/post-receive"
    assert os.path.exists(hook_path), f"The post-receive hook {hook_path} does not exist."
    assert os.access(hook_path, os.X_OK), f"The post-receive hook {hook_path} is not executable."

def test_alerts_log_generated():
    log_path = "/home/user/alerts.log"
    assert os.path.exists(log_path), f"The alerts log {log_path} does not exist. Did the git push trigger the hook?"

    with open(log_path, "r") as f:
        content = f.read()

    assert "ALERT: Network configuration changed" in content, "The alerts log does not contain the expected alert message."

def test_monitor_local_and_status():
    local_repo = "/home/user/monitor_local"
    status_file = os.path.join(local_repo, "status.txt")

    assert os.path.isdir(local_repo), f"The local repository {local_repo} does not exist."
    assert os.path.exists(status_file), f"The status file {status_file} does not exist."

    with open(status_file, "r") as f:
        content = f.read()

    expected_status = "Network check passed for /home/user/my_fstab"
    assert expected_status in content, f"The status file does not contain the expected output. Found: {content}"

def test_git_push_occurred():
    repo_path = "/home/user/monitor.git"
    # Verify that the status.txt file exists in the HEAD of the bare repository
    result = subprocess.run(
        ["git", "-C", repo_path, "ls-tree", "-r", "HEAD", "--name-only"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, "Failed to inspect the bare repository HEAD."
    assert "status.txt" in result.stdout.splitlines(), "status.txt was not pushed to the bare repository."