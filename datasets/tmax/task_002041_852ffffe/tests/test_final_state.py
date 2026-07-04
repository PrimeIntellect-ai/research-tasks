# test_final_state.py

import os
import re
import pytest
import subprocess

DEPLOY_LOG = "/home/user/deploy.log"
APP_STORAGE = "/home/user/app_storage"
CURRENT_PID_FILE = os.path.join(APP_STORAGE, "current.pid")
APP_LOG = os.path.join(APP_STORAGE, "app.log")

def test_deploy_script_exists_and_executable():
    script_path = "/home/user/deploy.sh"
    assert os.path.isfile(script_path), f"Deployment script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Deployment script {script_path} is not executable."

def test_deploy_log_contents():
    assert os.path.isfile(DEPLOY_LOG), f"Log file {DEPLOY_LOG} does not exist."
    with open(DEPLOY_LOG, "r") as f:
        log_content = f.read()

    assert re.search(r"\[SUCCESS\] Deployed v1\.tar\.gz with PID \d+", log_content), "v1.tar.gz success log missing or incorrect."
    assert re.search(r"\[FAILED\] v2\.tar\.gz - Security violation", log_content), "v2.tar.gz failure log missing or incorrect."
    assert re.search(r"\[FAILED\] v3\.tar\.gz - Quota exceeded", log_content), "v3.tar.gz failure log missing or incorrect."
    assert re.search(r"\[SUCCESS\] Deployed v4\.tar\.gz with PID \d+", log_content), "v4.tar.gz success log missing or incorrect."

def test_app_directories_state():
    assert os.path.isdir(os.path.join(APP_STORAGE, "app_v1")), "app_v1 directory should exist."
    assert os.path.isdir(os.path.join(APP_STORAGE, "app_v4")), "app_v4 directory should exist."

    assert not os.path.exists(os.path.join(APP_STORAGE, "app_v2")), "app_v2 directory should not exist (security violation)."
    assert not os.path.exists(os.path.join(APP_STORAGE, "app_v3")), "app_v3 directory should not exist (quota exceeded)."

def test_current_pid_and_process_state():
    assert os.path.isfile(CURRENT_PID_FILE), f"{CURRENT_PID_FILE} does not exist."

    with open(CURRENT_PID_FILE, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file does not contain a valid integer: {pid_str}"

    pid = int(pid_str)

    # Check if process is running
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} (from current.pid) is not running.")

    # Check if it's the v4 process (its run.sh should be in app_v4)
    try:
        cmdline_path = f"/proc/{pid}/cmdline"
        with open(cmdline_path, "r") as f:
            cmdline = f.read().replace('\x00', ' ')
        assert "app_v4" in cmdline or "run.sh" in cmdline, f"Running process {pid} does not appear to be v4. Cmdline: {cmdline}"
    except FileNotFoundError:
        pytest.fail(f"Could not read cmdline for process {pid}.")

def test_v1_process_not_running():
    # Parse the v1 PID from deploy.log
    with open(DEPLOY_LOG, "r") as f:
        log_content = f.read()

    match = re.search(r"\[SUCCESS\] Deployed v1\.tar\.gz with PID (\d+)", log_content)
    if match:
        v1_pid = int(match.group(1))
        try:
            os.kill(v1_pid, 0)
            pytest.fail(f"v1 process with PID {v1_pid} is still running. It should have been terminated.")
        except OSError:
            pass # Expected
    else:
        pytest.fail("Could not find v1 PID in deploy.log to verify it was killed.")

def test_app_log_output():
    assert os.path.isfile(APP_LOG), f"{APP_LOG} does not exist."
    with open(APP_LOG, "r") as f:
        log_content = f.read()

    assert "v1 running" in log_content, "v1 output missing from app.log"
    assert "v4 running" in log_content, "v4 output missing from app.log"