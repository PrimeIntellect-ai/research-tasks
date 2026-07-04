# test_final_state.py

import os
import urllib.request
import urllib.error
import subprocess
import pytest

APP_DIR = "/home/user/app"
SUCCESS_LOG = os.path.join(APP_DIR, "success.log")
TEST_STACK_PY = os.path.join(APP_DIR, "test_stack.py")

def test_success_log_exists_and_content():
    assert os.path.isfile(SUCCESS_LOG), f"Log file {SUCCESS_LOG} is missing."
    with open(SUCCESS_LOG, "r") as f:
        content = f.read().strip()

    expected_log = "STATUS: 200, BODY: Backend Active"
    assert expected_log in content, f"Expected '{expected_log}' in {SUCCESS_LOG}, but found:\n{content}"

def test_test_stack_script_exists():
    assert os.path.isfile(TEST_STACK_PY), f"Test script {TEST_STACK_PY} is missing."

def test_nginx_and_backend_running():
    try:
        req = urllib.request.Request("http://127.0.0.1:8080")
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.getcode()
            body = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx at http://127.0.0.1:8080: {e}")

    assert status == 200, f"Expected HTTP status 200, got {status}"
    assert body == "Backend Active", f"Expected body 'Backend Active', got '{body}'"

def test_processes_running():
    # Check if nginx and monitor.py are running
    ps_output = subprocess.check_output(["ps", "aux"]).decode("utf-8")

    nginx_running = "nginx" in ps_output
    monitor_running = "monitor.py" in ps_output

    assert nginx_running, "Nginx process is not running."
    assert monitor_running, "monitor.py process is not running."