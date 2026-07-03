# test_final_state.py

import os
import json
import time
import subprocess
import signal
import pytest

def test_service_env_exists_and_content():
    env_file = "/home/user/.service_env"
    assert os.path.isfile(env_file), f"Environment file {env_file} does not exist."
    with open(env_file, "r") as f:
        content = f.read()
    assert "API_KEY=sre_monitor_99" in content, "API_KEY is missing or incorrect in .service_env"
    assert "SERVICE_B_PORT=9090" in content, "SERVICE_B_PORT is missing or incorrect in .service_env"

def test_supervisor_exists():
    assert os.path.isfile("/home/user/supervisor.py"), "supervisor.py does not exist."

def test_supervisor_running():
    # Check if supervisor.py is running
    p = subprocess.run(["pgrep", "-f", "supervisor.py"], capture_output=True, text=True)
    assert p.returncode == 0, "supervisor.py is not running in the background."

def test_services_running():
    # Check if service_a.py and service_b.py are running
    p_a = subprocess.run(["pgrep", "-f", "service_a.py"], capture_output=True, text=True)
    assert p_a.returncode == 0, "service_a.py is not running."

    p_b = subprocess.run(["pgrep", "-f", "service_b.py"], capture_output=True, text=True)
    assert p_b.returncode == 0, "service_b.py is not running."

def test_monitor_status_json():
    status_file = "/home/user/monitor_status.json"
    assert os.path.isfile(status_file), f"{status_file} does not exist."

    with open(status_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{status_file} is not valid JSON.")

    assert "service_a" in data, "Missing 'service_a' in status JSON."
    assert "service_b" in data, "Missing 'service_b' in status JSON."
    assert "restarts" in data, "Missing 'restarts' in status JSON."
    assert data["service_a"] == "running", "service_a should be running."
    assert data["service_b"] == "running", "service_b should be running."
    assert isinstance(data["restarts"], int), "restarts should be an integer."

def test_log_rotation():
    log_dir = "/home/user/logs"
    assert os.path.isdir(log_dir), f"Log directory {log_dir} does not exist."

    log_file = os.path.join(log_dir, "services.log")
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist."

    # Wait a bit to ensure log rotation has a chance to occur since service_b prints rapidly
    time.sleep(2)

    rotated_log = os.path.join(log_dir, "services.log.1")
    assert os.path.isfile(rotated_log), f"Rotated log file {rotated_log} does not exist. Log rotation may not be working or size is incorrect."

    # Check size of rotated log
    size = os.path.getsize(rotated_log)
    # The size should be around 1024 bytes. We allow some buffer for line completion.
    assert 500 <= size <= 2048, f"Rotated log size is {size} bytes, expected around 1024 bytes."

def test_restart_functionality():
    status_file = "/home/user/monitor_status.json"
    with open(status_file, "r") as f:
        initial_data = json.load(f)
    initial_restarts = initial_data["restarts"]

    # Kill service_a
    p_a = subprocess.run(["pgrep", "-f", "service_a.py"], capture_output=True, text=True)
    if p_a.returncode == 0:
        pids = p_a.stdout.strip().split()
        for pid in pids:
            try:
                os.kill(int(pid), signal.SIGKILL)
            except ProcessLookupError:
                pass

    # Wait for supervisor to restart it
    time.sleep(3)

    # Check if it's running again
    p_a_new = subprocess.run(["pgrep", "-f", "service_a.py"], capture_output=True, text=True)
    assert p_a_new.returncode == 0, "service_a.py was not restarted by the supervisor."

    # Check if restarts count incremented
    with open(status_file, "r") as f:
        new_data = json.load(f)
    assert new_data["restarts"] > initial_restarts, "Restarts counter was not incremented in monitor_status.json after a process was killed."
    assert new_data["service_a"] == "running", "service_a status in JSON is not 'running' after restart."