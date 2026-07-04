# test_final_state.py
import os
import time
import glob
import requests
import pytest
import subprocess

def test_directory_structure():
    assert os.path.isdir("/home/user/gw/logs"), "/home/user/gw/logs does not exist"
    assert os.path.isdir("/home/user/gw/conf"), "/home/user/gw/conf does not exist"
    assert os.path.isdir("/home/user/gw/run"), "/home/user/gw/run does not exist"

def test_configuration_file():
    conf_path = "/home/user/gw/conf/settings.ini"
    assert os.path.isfile(conf_path), f"{conf_path} does not exist"
    with open(conf_path, "r") as f:
        content = f.read().strip()
    assert content == "target=127.0.0.1:9090", f"Configuration file content is incorrect: {content}"

def test_symlink():
    symlink_path = "/home/user/gw/active_conf"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink"
    assert os.readlink(symlink_path) == "/home/user/gw/conf/settings.ini", f"Symlink points to wrong location: {os.readlink(symlink_path)}"

def test_supervisor_script_exists():
    script_path = "/home/user/supervisor.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"

def test_gateway_executable_exists():
    exe_path = "/app/net-bridge-c/gateway"
    assert os.path.isfile(exe_path), f"Gateway executable not found at {exe_path}. Did compilation fail?"
    assert os.access(exe_path, os.X_OK), f"{exe_path} is not executable"

def test_service_running_and_supervisor_behavior():
    url_ping = "http://127.0.0.1:8888/ping"
    url_crash = "http://127.0.0.1:8888/crash"

    # Check if the service is up initially
    try:
        resp = requests.get(url_ping, timeout=2)
        assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"
        assert "PONG" in resp.text, f"Expected PONG in response, got: {resp.text}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to gateway at {url_ping}: {e}")

    # Trigger a crash
    try:
        requests.get(url_crash, timeout=2)
    except requests.RequestException:
        pass # Expected to fail or close connection abruptly

    # Wait for supervisor to restart it
    time.sleep(2)

    # Check if service is restored
    try:
        resp = requests.get(url_ping, timeout=2)
        assert resp.status_code == 200, f"Expected 200 OK after crash recovery, got {resp.status_code}"
        assert "PONG" in resp.text, f"Expected PONG in response after crash recovery, got: {resp.text}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to gateway after crash at {url_ping}. Supervisor did not restart it properly: {e}")

    # Check if backup log was created
    backup_logs = glob.glob("/home/user/gw/logs/gw.log.bak.*")
    assert len(backup_logs) > 0, "No backup log files found matching /home/user/gw/logs/gw.log.bak.* after crash"

def test_pid_file_exists():
    pid_path = "/home/user/gw/run/gw.pid"
    assert os.path.isfile(pid_path), f"PID file {pid_path} does not exist"
    with open(pid_path, "r") as f:
        pid = f.read().strip()
    assert pid.isdigit(), f"PID file contains invalid PID: {pid}"