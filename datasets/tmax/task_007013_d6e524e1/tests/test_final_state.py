# test_final_state.py
import os
import urllib.request
import re
import subprocess

def test_disk_monitor_running():
    executable_path = "/home/user/app/disk_monitor"
    assert os.path.exists(executable_path), f"{executable_path} executable does not exist"

    # Check if the process is running
    res = subprocess.run(['pgrep', '-f', 'disk_monitor'], stdout=subprocess.PIPE)
    assert res.returncode == 0, "disk_monitor process is not running"

def test_nginx_running():
    res = subprocess.run(['pgrep', '-f', 'nginx'], stdout=subprocess.PIPE)
    assert res.returncode == 0, "nginx process is not running"

def test_port_forwarding_and_app_response():
    try:
        req = urllib.request.urlopen("http://127.0.0.1:9090/", timeout=2)
        res = req.read().decode('utf-8')
    except Exception as e:
        assert False, f"Failed to connect to http://127.0.0.1:9090/ or read response: {e}. Ensure port forwarding is set up and the C app is bound to the correct socket."

    assert "RESOURCE_USAGE:" in res, f"Expected 'RESOURCE_USAGE:' in response, but got: {res}"

def test_check_capacity_script():
    script_path = "/home/user/check_capacity.sh"
    assert os.path.exists(script_path), f"{script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"

def test_capacity_log():
    log_path = "/home/user/capacity.log"
    assert os.path.exists(log_path), f"{log_path} does not exist. Did you run the check_capacity.sh script?"

    with open(log_path, "r") as f:
        content = f.read()

    # We expect a line like "[LOG] Usage is 88%"
    match = re.search(r"\[LOG\] Usage is \d+%", content)
    assert match is not None, f"Correct log entry format not found in {log_path}. Content was: {content}"