# test_final_state.py

import os
import subprocess
import json
import pytest

def test_setup_config_idempotent():
    """Verify that setup_config.sh is idempotent and creates the required files/directories."""
    script_path = "/home/user/setup_config.sh"
    assert os.path.exists(script_path), f"{script_path} does not exist."

    # Run the script twice to check idempotency
    subprocess.run(["bash", script_path], check=True)
    subprocess.run(["bash", script_path], check=True)

    assert os.path.isdir("/home/user/backup_mnt"), "/home/user/backup_mnt directory was not created."
    assert os.path.exists("/home/user/local_fstab"), "/home/user/local_fstab was not created."

    expected_line = "/dev/disk/by-label/BACKUP /home/user/backup_mnt ext4 rw,nosuid,nodev,noexec,auto,nouser,async 0 2"

    with open("/home/user/local_fstab", "r") as f:
        content = f.read()

    count = content.count(expected_line)
    assert count == 1, f"Expected exactly 1 occurrence of the fstab line, found {count}. The script might not be idempotent."

def test_git_repo_and_hook():
    """Verify the bare repository and the post-receive hook."""
    repo_path = "/home/user/config.git"
    assert os.path.isdir(repo_path), f"{repo_path} does not exist."

    # Check if it's a bare repo
    result = subprocess.run(["git", "-C", repo_path, "rev-parse", "--is-bare-repository"], capture_output=True, text=True)
    assert result.stdout.strip() == "true", f"{repo_path} is not a bare git repository."

    hook_path = os.path.join(repo_path, "hooks", "post-receive")
    assert os.path.exists(hook_path), f"Hook {hook_path} does not exist."
    assert os.access(hook_path, os.X_OK), f"Hook {hook_path} is not executable."

def test_alerts_log():
    """Verify that alerts.log contains the correct JSON logs for the push."""
    repo_path = "/home/user/config.git"
    log_path = "/home/user/alerts.log"

    assert os.path.exists(log_path), f"{log_path} does not exist."

    # Get the latest revision
    result = subprocess.run(["git", "-C", repo_path, "rev-parse", "refs/heads/master"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to get the latest revision from refs/heads/master."
    newrev = result.stdout.strip()

    expected_fstab_alert = json.dumps({
        "event": "alert",
        "reason": "critical_config_change",
        "file": "local_fstab",
        "revision": newrev
    })

    expected_backup_alert = json.dumps({
        "event": "alert",
        "reason": "critical_config_change",
        "file": "backup.sh",
        "revision": newrev
    })

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # We parse the JSON lines from the log to avoid strict string formatting issues (e.g. spacing)
    parsed_logs = []
    for line in lines:
        try:
            parsed_logs.append(json.loads(line))
        except json.JSONDecodeError:
            pass

    fstab_found = any(
        log.get("event") == "alert" and 
        log.get("reason") == "critical_config_change" and 
        log.get("file") == "local_fstab" and 
        log.get("revision") == newrev 
        for log in parsed_logs
    )

    backup_found = any(
        log.get("event") == "alert" and 
        log.get("reason") == "critical_config_change" and 
        log.get("file") == "backup.sh" and 
        log.get("revision") == newrev 
        for log in parsed_logs
    )

    assert fstab_found, f"alerts.log does not contain the expected alert for local_fstab with revision {newrev}."
    assert backup_found, f"alerts.log does not contain the expected alert for backup.sh with revision {newrev}."