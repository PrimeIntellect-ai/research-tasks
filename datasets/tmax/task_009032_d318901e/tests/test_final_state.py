# test_final_state.py

import os
import json
import urllib.request
import subprocess
import pytest

SHARED_DATA_DIR = "/home/user/shared_data"
ACL_REPORT = "/home/user/acl_report.txt"
CAPACITY_REPORT = "/home/user/capacity_report.json"

def test_acl_applied():
    """Check if the ACL is correctly applied to the directory."""
    result = subprocess.run(['getfacl', SHARED_DATA_DIR], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to run getfacl."
    assert "user:nobody:r-x" in result.stdout, f"ACL for 'nobody' is not correctly set on {SHARED_DATA_DIR}."

def test_acl_report():
    """Check if the acl_report.txt contains the correct ACL entry."""
    assert os.path.isfile(ACL_REPORT), f"{ACL_REPORT} does not exist."
    with open(ACL_REPORT, 'r') as f:
        content = f.read()
    assert "user:nobody:r-x" in content, f"{ACL_REPORT} does not contain 'user:nobody:r-x'."

def test_capacity_report():
    """Check if capacity_report.json exists and has correct format."""
    assert os.path.isfile(CAPACITY_REPORT), f"{CAPACITY_REPORT} does not exist."
    with open(CAPACITY_REPORT, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{CAPACITY_REPORT} is not valid JSON.")

    assert "usage_bytes" in data, f"{CAPACITY_REPORT} missing 'usage_bytes' key."
    assert isinstance(data["usage_bytes"], int), f"'usage_bytes' in {CAPACITY_REPORT} is not an integer."
    assert data["usage_bytes"] > 0, f"'usage_bytes' should be greater than 0."

def test_port_9090_responds():
    """Check if the HTTP server on port 9090 is running and returns the correct JSON."""
    try:
        with urllib.request.urlopen("http://127.0.0.1:9090/", timeout=2) as response:
            assert response.status == 200, "Expected HTTP 200 OK from port 9090."
            data = json.loads(response.read().decode())
            assert "usage_bytes" in data, "Response from 9090 missing 'usage_bytes' key."
            assert isinstance(data["usage_bytes"], int), "'usage_bytes' from 9090 is not an integer."
    except Exception as e:
        pytest.fail(f"Failed to connect to or read from 127.0.0.1:9090. Error: {e}")

def test_port_8080_responds():
    """Check if the forwarded port 8080 is running and returns the correct JSON."""
    try:
        with urllib.request.urlopen("http://127.0.0.1:8080/", timeout=2) as response:
            assert response.status == 200, "Expected HTTP 200 OK from port 8080."
            data = json.loads(response.read().decode())
            assert "usage_bytes" in data, "Response from 8080 missing 'usage_bytes' key."
            assert isinstance(data["usage_bytes"], int), "'usage_bytes' from 8080 is not an integer."
    except Exception as e:
        pytest.fail(f"Failed to connect to or read from 127.0.0.1:8080. Error: {e}")

def test_monitor_script_exists():
    """Check if the monitoring script exists."""
    py_exists = os.path.isfile("/home/user/monitor.py")
    js_exists = os.path.isfile("/home/user/monitor.js")
    assert py_exists or js_exists, "Monitoring script (monitor.py or monitor.js) not found in /home/user/."