# test_final_state.py

import os
import json
import urllib.request
import ssl
import pytest

def test_final_report_json():
    """Check if /home/user/final_report.json exists and is formatted correctly."""
    report_path = "/home/user/final_report.json"
    assert os.path.exists(report_path), f"{report_path} does not exist."

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{report_path} is not valid JSON.")

    assert "alert_file_content" in data, "Missing 'alert_file_content' in final_report.json"
    assert "service_recovered" in data, "Missing 'service_recovered' in final_report.json"

    assert data["alert_file_content"] == "ALERT: Service down", f"Expected alert_file_content to be 'ALERT: Service down', got '{data['alert_file_content']}'"
    assert data["service_recovered"] is True, f"Expected service_recovered to be true, got {data['service_recovered']}"

def test_symlink_exists():
    """Verify /home/user/monitor_alert_sys/docroot/health.json is a symlink pointing to /home/user/system_status.json."""
    symlink_path = "/home/user/monitor_alert_sys/docroot/health.json"
    target_path = "/home/user/system_status.json"

    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."
    assert os.readlink(symlink_path) == target_path, f"{symlink_path} does not point to {target_path}."

def test_server_running_and_responds():
    """Perform an HTTPS GET request to ensure the server is actively running and responds with {"status": "ok"}."""
    url = "https://127.0.0.1:8443/health.json"

    # Ignore self-signed certificate warnings
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            body = response.read().decode('utf-8')
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                pytest.fail("Response body is not valid JSON.")
            assert data.get("status") == "ok", f"Expected {{'status': 'ok'}}, got {data}"
    except Exception as e:
        pytest.fail(f"Failed to connect to {url} or read response: {e}")

def test_pid_file_and_process():
    """Check that /home/user/monitor_alert_sys/server.pid exists and contains the PID of a running Python process."""
    pid_file = "/home/user/monitor_alert_sys/server.pid"
    assert os.path.exists(pid_file), f"{pid_file} does not exist."

    with open(pid_file, 'r') as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file does not contain a valid integer: '{pid_str}'"
    pid = int(pid_str)

    # Check if process is running
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} is not running.")

    # Check if it's a python process (optional but good for robustness)
    comm_file = f"/proc/{pid}/comm"
    if os.path.exists(comm_file):
        with open(comm_file, 'r') as f:
            comm = f.read().strip()
            assert "python" in comm.lower(), f"Process {pid} is running but does not appear to be Python (comm: {comm})."

def test_alert_file():
    """Verify /home/user/monitor_alert_sys/alerts/latest_alert.txt exists and contains 'ALERT: Service down'."""
    alert_file = "/home/user/monitor_alert_sys/alerts/latest_alert.txt"
    assert os.path.exists(alert_file), f"{alert_file} does not exist."

    with open(alert_file, 'r') as f:
        content = f.read().strip()

    assert content == "ALERT: Service down", f"Expected alert file content to be 'ALERT: Service down', got '{content}'"