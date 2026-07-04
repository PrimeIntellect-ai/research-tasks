# test_final_state.py

import os
import urllib.request
import urllib.parse
import json
import time

def test_libexpr_so_exists():
    assert os.path.isfile("/home/user/workspace/libexpr.so"), "/home/user/workspace/libexpr.so does not exist. Did you compile the C library?"

def test_server_py_exists():
    assert os.path.isfile("/home/user/workspace/server.py"), "/home/user/workspace/server.py does not exist."

def test_status_ready():
    status_file = "/home/user/workspace/status.txt"
    assert os.path.isfile(status_file), f"{status_file} does not exist. Did you write READY to it?"
    with open(status_file, "r") as f:
        content = f.read().strip()
    assert content == "READY", f"Expected 'READY' in {status_file}, got '{content}'"

def test_web_server_logic():
    # Send a request to the web server
    url = "http://127.0.0.1:8080/organize?prefix=dataset_&expr=3%2B4&dest=reports"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            status_code = response.getcode()
            body = response.read().decode('utf-8')
    except Exception as e:
        assert False, f"Failed to connect to the server or server returned an error: {e}"

    assert status_code == 200, f"Expected HTTP status 200, got {status_code}"

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        assert False, f"Response body is not valid JSON: {body}"

    expected_data = {"status": "success", "file": "dataset_7.dat", "destination": "reports"}
    assert data == expected_data, f"Expected JSON response {expected_data}, got {data}"

    # Verify file was moved
    organized_file = "/home/user/workspace/organized/reports/dataset_7.dat"
    inbox_file = "/home/user/workspace/inbox/dataset_7.dat"

    assert os.path.isfile(organized_file), f"Expected file to be moved to {organized_file}, but it is not there."
    assert not os.path.exists(inbox_file), f"Expected file {inbox_file} to be removed from inbox, but it still exists."