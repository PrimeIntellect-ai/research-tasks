# test_final_state.py

import os
import time
import subprocess
import urllib.request
import signal

def test_nginx_conf_fixed():
    path = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    assert "proxy_pass http://unix:/home/user/run/app.sock;" in content, \
        "The Nginx configuration does not point to the correct upstream socket path (/home/user/run/app.sock)."

def test_supervise_script_exists():
    path = "/home/user/supervise.sh"
    assert os.path.isfile(path), f"Supervisor script {path} is missing."

def test_nginx_serving_backend():
    try:
        req = urllib.request.Request("http://localhost:8080")
        with urllib.request.urlopen(req, timeout=5) as response:
            body = response.read().decode("utf-8")
            assert "Backend Alive" in body, "Nginx did not return the expected success message from the backend."
    except Exception as e:
        assert False, f"Failed to connect to Nginx on port 8080 or unexpected response: {e}"

def get_backend_pids():
    try:
        output = subprocess.check_output(["pgrep", "-f", "backend.py"]).decode("utf-8")
        return [int(pid) for pid in output.strip().split("\n") if pid]
    except subprocess.CalledProcessError:
        return []

def test_supervisor_restarts_backend_and_logs():
    pids = get_backend_pids()
    assert len(pids) > 0, "backend.py is not currently running."

    # Kill the backend processes
    for pid in pids:
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass

    # Wait for supervisor to restart it
    time.sleep(3)

    new_pids = get_backend_pids()
    assert len(new_pids) > 0, "backend.py was not restarted by the supervisor after being killed."

    # Ensure it's a new process
    for pid in pids:
        assert pid not in new_pids, "backend.py has the same PID, it was not actually killed or restarted properly."

    # Check the log file
    log_path = "/home/user/supervise.log"
    assert os.path.isfile(log_path), f"Log file {log_path} was not created."

    with open(log_path, "r") as f:
        log_content = f.read()

    assert "[CRASH] restarted backend" in log_content, \
        f"The exact string '[CRASH] restarted backend' was not found in {log_path}."