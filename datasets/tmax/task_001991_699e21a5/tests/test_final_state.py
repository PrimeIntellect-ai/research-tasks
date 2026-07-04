# test_final_state.py

import os
import json
import pytest

def test_bare_repo_exists():
    """Verify the bare git repository exists."""
    assert os.path.isdir("/home/user/dashboards.git/objects"), "Bare Git repository at /home/user/dashboards.git does not exist or is not a bare repo."

def test_hook_executable():
    """Verify the post-receive hook exists and is executable."""
    hook_path = "/home/user/dashboards.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Hook file {hook_path} does not exist."
    assert os.access(hook_path, os.X_OK), f"Hook file {hook_path} is not executable."

def test_alert_service_running():
    """Verify the Rust service PID file exists and the process is running."""
    pid_file = "/home/user/alert_service.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} does not exist."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid numeric PID."

    pid = int(pid_str)
    # Check if process is running by sending signal 0
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} from {pid_file} is not running.")

def test_alert_log_content():
    """Verify the dashboard commit triggered the alert log."""
    log_file = "/home/user/dashboard_alerts.log"
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist."

    with open(log_file, "r") as f:
        content = f.read()

    assert "ALERT: Dashboards updated" in content, f"Log file {log_file} does not contain the expected alert string."

def test_work_repo_content():
    """Verify the clone exists and contains the correct dashboard."""
    dashboard_file = "/home/user/dashboards_work/network_dashboard.json"
    assert os.path.isfile(dashboard_file), f"Dashboard file {dashboard_file} does not exist."

    with open(dashboard_file, "r") as f:
        content = f.read()

    assert "Network Metrics" in content, f"Dashboard file {dashboard_file} does not contain 'Network Metrics'."

    # Optional: verify it's valid JSON
    try:
        data = json.loads(content)
        assert data.get("title") == "Network Metrics", "JSON title is not 'Network Metrics'."
    except json.JSONDecodeError:
        pytest.fail(f"Dashboard file {dashboard_file} does not contain valid JSON.")