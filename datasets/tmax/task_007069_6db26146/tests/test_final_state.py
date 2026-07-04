# test_final_state.py

import os
import urllib.request
import urllib.error
import glob
import pytest

def test_symlink_fixed():
    symlink_path = "/home/user/app/data"
    assert os.path.islink(symlink_path), f"Expected {symlink_path} to be a symlink."
    target = os.readlink(symlink_path)
    assert target == "/home/user/shared_data", f"Symlink {symlink_path} points to {target}, expected /home/user/shared_data."

def test_app_running():
    url = "http://127.0.0.1:8080/ping"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.getcode()
            content = response.read().decode('utf-8').strip()
            assert status == 200, f"Expected HTTP 200 OK, got {status}."
            assert "pong" in content, f"Expected 'pong' in response, got '{content}'."
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to the application at {url}: {e}")

def test_health_log():
    log_path = "/home/user/health.log"
    assert os.path.isfile(log_path), f"Health log file {log_path} is missing."
    with open(log_path, "r") as f:
        content = f.read()
    assert "STATUS: OK" in content, f"Expected 'STATUS: OK' in {log_path}, but it was not found."

def test_health_check_script_exists():
    # The health check script can have any extension, so we use glob
    scripts = glob.glob("/home/user/health_check*")
    assert len(scripts) > 0, "Health check script starting with '/home/user/health_check' is missing."

    # At least one of them should be a file
    valid_scripts = [s for s in scripts if os.path.isfile(s)]
    assert len(valid_scripts) > 0, "Health check script must be a valid file."