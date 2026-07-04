# test_final_state.py

import os
import urllib.request
import pytest

def test_health_monitor_c_updated():
    c_file = "/home/user/restore/health_monitor.c"
    assert os.path.isfile(c_file), f"File missing: {c_file}"
    with open(c_file, "r") as f:
        content = f.read()
    assert '127.0.0.1' in content, "health_monitor.c does not contain the updated IP address '127.0.0.1'"
    assert '192.0.2.100' not in content, "health_monitor.c still contains the old IP address '192.0.2.100'"

def test_monitor_daemon_compiled():
    daemon_path = "/home/user/restore/monitor_daemon"
    assert os.path.isfile(daemon_path), f"Compiled executable missing: {daemon_path}"
    assert os.access(daemon_path, os.X_OK), f"File is not executable: {daemon_path}"

def test_health_report_log_exists_and_correct():
    log_path = "/home/user/health_report.log"
    assert os.path.isfile(log_path), f"Output log file missing: {log_path}"

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_content = "SYSTEM_HEALTHY: Service reachable at 127.0.0.1:9090"
    assert expected_content in content, f"Log file content is incorrect. Expected to find '{expected_content}', but got '{content}'"

def test_daemon_running_and_reachable():
    # Verify the daemon is actually running on port 8080
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/status")
        with urllib.request.urlopen(req, timeout=2) as response:
            body = response.read().decode('utf-8')
            assert "SYSTEM_HEALTHY: Service reachable at 127.0.0.1:9090" in body, "Daemon is running but returned unexpected content"
    except Exception as e:
        pytest.fail(f"Could not reach the monitor daemon on 127.0.0.1:8080. Is it running? Error: {e}")