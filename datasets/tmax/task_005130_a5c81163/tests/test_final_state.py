# test_final_state.py

import os
import time
import urllib.request
import urllib.error
import subprocess
import pytest
import stat

PROJECT_DIR = "/home/user/infra_project"

def test_deploy_script_exists_and_executable():
    """Verify deploy.sh exists and is executable."""
    deploy_script = os.path.join(PROJECT_DIR, "deploy.sh")
    assert os.path.isfile(deploy_script), f"{deploy_script} does not exist."
    st = os.stat(deploy_script)
    assert bool(st.st_mode & stat.S_IXUSR), f"{deploy_script} is not executable."

def test_execution_and_initial_state():
    """Run deploy.sh, verify port forwarding, init, and server startup."""
    deploy_script = os.path.join(PROJECT_DIR, "deploy.sh")

    # Run the deploy script
    subprocess.run(["bash", deploy_script], check=True)

    # Wait for services to start
    time.sleep(3)

    # Check data extraction and API availability through port forward
    try:
        req = urllib.request.Request("http://127.0.0.1:9090/api/data")
        with urllib.request.urlopen(req, timeout=5) as response:
            data = response.read().decode('utf-8')
            assert '{"status": "recovered"}' in data, "API did not return expected restored data."
    except Exception as e:
        pytest.fail(f"Failed to connect to API on port 9090: {e}. Check port forwarding and initialization.")

def test_supervisor_restart_and_logging():
    """Crash the server, verify supervisor restarts it, and check logs."""
    # Crash the server
    try:
        urllib.request.urlopen("http://127.0.0.1:9090/crash", timeout=2)
    except Exception:
        pass  # Expected to fail/timeout on crash

    # Wait for supervisor to detect and restart
    time.sleep(4)

    # Check if server is back up
    try:
        req = urllib.request.Request("http://127.0.0.1:9090/health")
        with urllib.request.urlopen(req, timeout=5) as response:
            data = response.read().decode('utf-8')
            assert data == "healthy", "Server did not return 'healthy' after restart."
    except Exception as e:
        pytest.fail(f"Server did not recover after crash. Supervisor might be failing. Error: {e}")

    # Check server.log for restart messages
    server_log = os.path.join(PROJECT_DIR, "logs/server.log")
    assert os.path.isfile(server_log), "server.log does not exist."
    with open(server_log, "r") as f:
        content = f.read()
        occurrences = content.count("Starting server")
        assert occurrences >= 2, f"Expected at least 2 'Starting server' messages in server.log, found {occurrences}."

def test_health_monitor_logging():
    """Verify health monitor is appending OK to health.log."""
    health_log = os.path.join(PROJECT_DIR, "logs/health.log")
    assert os.path.isfile(health_log), "health.log does not exist."
    with open(health_log, "r") as f:
        content = f.read()
        assert "OK" in content, "Health monitor is not logging 'OK' to health.log."

def test_logrotate_configuration():
    """Trigger logrotate manually and verify rotation and compression."""
    logrotate_conf = os.path.join(PROJECT_DIR, "logrotate.conf")
    logrotate_status = os.path.join(PROJECT_DIR, "logrotate.status")

    assert os.path.isfile(logrotate_conf), "logrotate.conf does not exist."

    # Run logrotate forcefully
    result = subprocess.run(
        ["logrotate", "-s", logrotate_status, "-f", logrotate_conf],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"logrotate failed: {result.stderr}"

    # Verify rotated logs exist (e.g., server.log.1.gz)
    logs_dir = os.path.join(PROJECT_DIR, "logs")
    rotated_files = [f for f in os.listdir(logs_dir) if "server.log.1" in f or "health.log.1" in f]

    assert len(rotated_files) > 0, "No rotated log files found after forcing logrotate."

    compressed = any(f.endswith(".gz") for f in rotated_files)
    assert compressed, "Rotated log files are not compressed (.gz expected)."