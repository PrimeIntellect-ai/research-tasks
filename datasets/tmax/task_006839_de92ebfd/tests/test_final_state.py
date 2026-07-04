# test_final_state.py

import os
import json
import time
import pytest
import subprocess

DASHBOARD_JSON = "/home/user/dashboard.json"
STATUS_JSON = "/home/user/status.json"
SUPERVISOR_PID_FILE = "/home/user/supervisor.pid"
SUPERVISE_LOG = "/home/user/supervise.log"
CRASH_FILE = "/home/user/crash_now"
DEPLOY_SH = "/home/user/deploy.sh"

def test_dashboard_json_updated():
    """Verify that update_dash.py correctly modified dashboard.json."""
    assert os.path.exists(DASHBOARD_JSON), f"Missing {DASHBOARD_JSON}"

    with open(DASHBOARD_JSON, 'r') as f:
        data = json.load(f)

    users = data.get("users", [])
    obs_admin_found = any(u.get("username") == "obs_admin" and u.get("group") == "obs_group" for u in users)
    assert obs_admin_found, "User 'obs_admin' with group 'obs_group' not found in users list."

    targets = data.get("monitored_targets", [])
    assert "127.0.0.1:8001" in targets, "127.0.0.1:8001 is missing from monitored_targets."
    assert "127.0.0.1:8002" in targets, "127.0.0.1:8002 is missing from monitored_targets."

def test_deploy_sh_executable():
    """Verify deploy.sh is executable."""
    assert os.path.exists(DEPLOY_SH), f"Missing {DEPLOY_SH}"
    assert os.access(DEPLOY_SH, os.X_OK), f"{DEPLOY_SH} is not executable."

def test_supervisor_running():
    """Verify that supervisor.pid contains a valid running PID."""
    assert os.path.exists(SUPERVISOR_PID_FILE), f"Missing {SUPERVISOR_PID_FILE}"

    with open(SUPERVISOR_PID_FILE, 'r') as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {SUPERVISOR_PID_FILE} does not contain a valid integer."
    pid = int(pid_str)

    # Check if process is running
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} from {SUPERVISOR_PID_FILE} is not running.")

def test_status_json_content():
    """Verify status.json contains the correct connectivity results."""
    # Give it a moment to ensure check_targets.py has written the file
    for _ in range(10):
        if os.path.exists(STATUS_JSON):
            break
        time.sleep(0.5)

    assert os.path.exists(STATUS_JSON), f"Missing {STATUS_JSON}"

    with open(STATUS_JSON, 'r') as f:
        status = json.load(f)

    assert status.get("127.0.0.1:9090") == "DOWN", "Expected 127.0.0.1:9090 to be DOWN"
    assert status.get("127.0.0.1:8001") == "UP", "Expected 127.0.0.1:8001 to be UP"
    assert status.get("127.0.0.1:8002") == "DOWN", "Expected 127.0.0.1:8002 to be DOWN"

def test_supervision_crash_recovery():
    """Test process supervision by triggering a crash and verifying recovery."""
    # Read initial log lines if any
    initial_restarts = 0
    if os.path.exists(SUPERVISE_LOG):
        with open(SUPERVISE_LOG, 'r') as f:
            initial_restarts = f.read().splitlines().count("RESTARTED")

    # Trigger a crash
    with open(CRASH_FILE, 'w') as f:
        f.write("crash")

    # Wait for the crash to be detected and restarted (max 5 seconds)
    restarted = False
    for _ in range(10):
        time.sleep(0.5)
        if os.path.exists(SUPERVISE_LOG):
            with open(SUPERVISE_LOG, 'r') as f:
                current_restarts = f.read().splitlines().count("RESTARTED")
                if current_restarts > initial_restarts:
                    restarted = True
                    break

    assert restarted, "Supervisor did not log 'RESTARTED' after triggering a crash."
    assert not os.path.exists(CRASH_FILE), f"Crash file {CRASH_FILE} was not deleted by the agent."