# test_final_state.py
import os
import time
import urllib.request
import subprocess
import pytest

def test_expect_script_exists():
    assert os.path.isfile("/home/user/automate_init.exp"), "/home/user/automate_init.exp does not exist"

def test_server_conf_contents():
    conf_path = "/home/user/server.conf"
    assert os.path.isfile(conf_path), f"{conf_path} does not exist"
    with open(conf_path, "r") as f:
        content = f.read()
    assert "PORT=8080" in content, "server.conf does not contain PORT=8080"
    assert "DIR=/home/user/webroot" in content, "server.conf does not contain DIR=/home/user/webroot"

def test_webroot_and_index():
    index_path = "/home/user/webroot/index.html"
    assert os.path.isfile(index_path), f"{index_path} does not exist"
    with open(index_path, "r") as f:
        content = f.read()
    assert "AutoProvisionedWeb" in content, "index.html does not contain AutoProvisionedWeb"

def get_python_server_pid():
    try:
        output = subprocess.check_output(["pgrep", "-f", "python3 -m http.server 8080"]).decode().strip()
        pids = output.split('\n')
        return [int(pid) for pid in pids if pid]
    except subprocess.CalledProcessError:
        return []

def test_server_running_and_watchdog_behavior():
    # Check if server is accessible
    try:
        with urllib.request.urlopen("http://localhost:8080/", timeout=2) as response:
            html = response.read().decode()
            assert "AutoProvisionedWeb" in html, "HTTP server not serving expected content"
    except Exception as e:
        pytest.fail(f"Could not connect to HTTP server on port 8080: {e}")

    # Find the python process
    pids = get_python_server_pid()
    assert pids, "Python HTTP server process not found"

    # Kill the process to trigger watchdog
    for pid in pids:
        try:
            os.kill(pid, 9)
        except ProcessLookupError:
            pass

    # Wait for watchdog to restart it
    time.sleep(3)

    # Check if server is accessible again
    try:
        with urllib.request.urlopen("http://localhost:8080/", timeout=2) as response:
            html = response.read().decode()
            assert "AutoProvisionedWeb" in html, "HTTP server not serving expected content after restart"
    except Exception as e:
        pytest.fail(f"Watchdog failed to restart the HTTP server: {e}")

    # Check log file
    log_path = "/home/user/watchdog.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist"
    with open(log_path, "r") as f:
        log_content = f.read()
    assert "[RESTART] python http server crashed, restarting..." in log_content, "Watchdog log does not contain the expected restart message"