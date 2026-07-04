# test_final_state.py

import os
import re
import stat
import subprocess
import pytest

def test_monitor_profile_exists_and_correct():
    profile_path = "/home/user/.monitor_profile"
    assert os.path.isfile(profile_path), f"File {profile_path} does not exist."

    with open(profile_path, "r") as f:
        content = f.read()

    # Check for LOG_DIR
    assert re.search(r'(export\s+LOG_DIR=|LOG_DIR=.*?export\s+LOG_DIR)', content) is not None, "LOG_DIR is not properly exported."
    assert "LOG_DIR=/home/user/service_logs" in content or "LOG_DIR=\"/home/user/service_logs\"" in content or "LOG_DIR='/home/user/service_logs'" in content, "LOG_DIR is not set to /home/user/service_logs."

    # Check for ALERT_THRESHOLD
    assert re.search(r'(export\s+ALERT_THRESHOLD=|ALERT_THRESHOLD=.*?export\s+ALERT_THRESHOLD)', content) is not None, "ALERT_THRESHOLD is not properly exported."
    assert "ALERT_THRESHOLD=10" in content or "ALERT_THRESHOLD=\"10\"" in content or "ALERT_THRESHOLD='10'" in content, "ALERT_THRESHOLD is not set to 10."

def test_alert_pipeline_script_executable():
    script_path = "/home/user/monitor_repo/alert_pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_active_alerts_log_correct():
    log_path = "/home/user/active_alerts.log"
    assert os.path.isfile(log_path), f"Alerts log {log_path} does not exist. Did you run the script?"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "ALERT: db failure rate at 20%",
        "ALERT: web failure rate at 15%"
    ]

    assert lines == expected_lines, f"Expected alerts to be exactly {expected_lines}, but got {lines}. Ensure alphabetical sorting and correct threshold/calculation."

def test_git_repo_and_pre_commit_hook():
    git_dir = "/home/user/monitor_repo/.git"
    assert os.path.isdir(git_dir), "Git repository was not initialized in /home/user/monitor_repo."

    hook_path = os.path.join(git_dir, "hooks", "pre-commit")
    assert os.path.isfile(hook_path), f"Pre-commit hook {hook_path} does not exist."

    st = os.stat(hook_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Pre-commit hook {hook_path} is not executable."

    with open(hook_path, "r") as f:
        content = f.read()

    assert "bash -n" in content or "bash --noexec" in content, "Pre-commit hook does not seem to contain 'bash -n' or equivalent syntax check."