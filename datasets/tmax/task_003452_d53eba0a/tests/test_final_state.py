# test_final_state.py

import os
import stat
import subprocess
import time
import pytest

def test_config_updated():
    config_path = "/home/user/proxy/config.env"
    assert os.path.isfile(config_path), f"{config_path} is missing."
    with open(config_path, "r") as f:
        content = f.read()
    assert "UPSTREAM_SOCKET=/home/user/run/backend_v2.sock" in content, "The UPSTREAM_SOCKET in config.env was not updated to backend_v2.sock."

def test_deployment_result_log():
    log_path = "/home/user/deployment_result.log"
    assert os.path.isfile(log_path), f"{log_path} is missing. Did you run deploy.sh?"
    with open(log_path, "r") as f:
        content = f.read()
    assert "200 OK: Backend Healthy" in content, f"Expected successful health check message in {log_path}, got: {content}"

def test_storage_monitor_log_size():
    log_path = "/home/user/logs/backend.log"
    assert os.path.isfile(log_path), f"{log_path} is missing. The backend server might not be running."

    # Wait briefly to allow the monitor to truncate if it just crossed the threshold
    time.sleep(2.5)

    size = os.path.getsize(log_path)
    # The monitor should truncate at 50000 bytes. With aggressive logging, it might grow a bit
    # before the next check, but should stay well under 200000 bytes.
    assert size < 200000, f"Log file size is {size} bytes, which exceeds the expected threshold. The storage monitor is not working correctly."

def test_scripts_executable():
    monitor_script = "/home/user/storage_monitor.sh"
    deploy_script = "/home/user/deploy.sh"

    assert os.path.isfile(monitor_script), f"{monitor_script} is missing."
    assert os.path.isfile(deploy_script), f"{deploy_script} is missing."

    st_monitor = os.stat(monitor_script)
    assert bool(st_monitor.st_mode & stat.S_IXUSR), f"{monitor_script} is not executable."

    st_deploy = os.stat(deploy_script)
    assert bool(st_deploy.st_mode & stat.S_IXUSR), f"{deploy_script} is not executable."

def test_processes_running():
    # Check if the required processes are running
    try:
        ps_output = subprocess.check_output(["ps", "-ef"]).decode("utf-8")
    except subprocess.CalledProcessError:
        pytest.fail("Failed to execute ps command.")

    assert "storage_monitor.sh" in ps_output, "storage_monitor.sh is not running in the background."
    assert "server.sh" in ps_output, "server.sh is not running in the background."

    # Check if the unix socket was created
    sock_path = "/home/user/run/backend_v2.sock"
    assert os.path.exists(sock_path), f"Unix socket {sock_path} does not exist."
    assert stat.S_ISSOCK(os.stat(sock_path).st_mode), f"{sock_path} is not a socket."