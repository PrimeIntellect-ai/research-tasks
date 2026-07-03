# test_final_state.py

import os
import time
import subprocess
import socket
import pytest

def test_fast_provision_executable():
    path = "/home/user/fast_provision.py"
    assert os.path.isfile(path), f"Missing file: {path}"
    assert os.access(path, os.X_OK), f"File is not executable: {path}"

def test_provisioning_speedup_and_success():
    fast_script = "/home/user/fast_provision.py"

    # Kill any existing services to ensure a cold start for accurate timing
    subprocess.run(["pkill", "-f", "redis-server"], capture_output=True)
    subprocess.run(["pkill", "-f", "auth_api"], capture_output=True)
    subprocess.run(["pkill", "-f", "worker_daemon"], capture_output=True)
    if os.path.exists("/tmp/worker_health.sock"):
        try:
            os.remove("/tmp/worker_health.sock")
        except OSError:
            pass

    # Measure fast_provision.py
    start_time = time.time()
    result = subprocess.run([fast_script], capture_output=True, text=True)
    end_time = time.time()

    fast_duration = end_time - start_time

    assert result.returncode == 0, f"fast_provision.py failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

    # The slow script takes ~15 seconds. We need a speedup of >= 2.5x.
    # 15 / 2.5 = 6.0 seconds.
    threshold = 6.0
    assert fast_duration <= threshold, f"Speedup metric failed: fast_provision.py took {fast_duration:.2f}s, which is not >= 2.5x speedup (must be <= {threshold}s)."

def test_services_running():
    # Check Redis
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        result = s.connect_ex(('127.0.0.1', 6379))
        assert result == 0, "Redis is not listening on port 6379"

    # Check Auth API
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        result = s.connect_ex(('127.0.0.1', 8080))
        assert result == 0, "Auth API is not listening on port 8080"

    # Check Worker socket
    assert os.path.exists("/tmp/worker_health.sock"), "Worker health socket /tmp/worker_health.sock does not exist"
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        result = s.connect_ex("/tmp/worker_health.sock")
        assert result == 0, "Cannot connect to Worker health socket at /tmp/worker_health.sock"

def test_provision_log():
    log_path = "/home/user/provision.log"
    assert os.path.isfile(log_path), f"Log file missing: {log_path}"
    with open(log_path, "r") as f:
        content = f.read()
    assert "Cluster initialized successfully." in content, "Log file does not contain the expected success message from admin_cli.py"

def test_crontab_configured():
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab"

    expected_cron = "*/5 * * * * /app/health_check.py"
    assert expected_cron in result.stdout, f"Crontab does not contain the expected entry. Found:\n{result.stdout}"