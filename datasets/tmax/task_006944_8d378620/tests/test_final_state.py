# test_final_state.py

import os
import re
import urllib.request
import subprocess
import time

def test_watchdog_log_exists_and_content():
    log_path = "/home/user/logs/watchdog.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) >= 2, f"Log file {log_path} must contain at least two lines."

    ok_regex = re.compile(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] STATUS: OK$")
    restarted_regex = re.compile(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] STATUS: RESTARTED$")

    has_ok = any(ok_regex.match(line) for line in lines)
    has_restarted = any(restarted_regex.match(line) for line in lines)

    assert has_ok, "Log file missing 'STATUS: OK' line matching the required format."
    assert has_restarted, "Log file missing 'STATUS: RESTARTED' line matching the required format."

def test_app_health_endpoint():
    url = "http://127.0.0.1:8080/health"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            status = response.getcode()
            body = response.read().decode("utf-8").strip()
    except Exception as e:
        assert False, f"Failed to connect to {url}: {e}"

    assert status == 200, f"Expected HTTP 200 from {url}, got {status}."
    assert body == "OK", f"Expected response body 'OK' from {url}, got '{body}'."

def test_pid_file_exists_and_accurate():
    pid_file = "/home/user/app/app.pid"
    assert os.path.exists(pid_file), f"PID file {pid_file} does not exist."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid integer."
    pid = int(pid_str)

    # Check if process is running
    try:
        os.kill(pid, 0)
    except OSError:
        assert False, f"Process with PID {pid} from {pid_file} is not running."

def test_deploy_idempotency():
    pid_file = "/home/user/app/app.pid"
    assert os.path.exists(pid_file), f"PID file {pid_file} does not exist."

    with open(pid_file, "r") as f:
        initial_pid = f.read().strip()

    deploy_script = "/home/user/deploy.py"
    assert os.path.exists(deploy_script), f"Deploy script {deploy_script} does not exist."

    result = subprocess.run(["python3", deploy_script], capture_output=True, text=True)
    assert result.returncode == 0, f"deploy.py failed with return code {result.returncode}."

    with open(pid_file, "r") as f:
        new_pid = f.read().strip()

    assert initial_pid == new_pid, "deploy.py is not idempotent: PID changed after running deploy.py again."