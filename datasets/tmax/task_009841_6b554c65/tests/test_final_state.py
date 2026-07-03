# test_final_state.py

import os
import json
import urllib.request
import urllib.error
import pytest

def test_poison_input_identified():
    path = "/home/user/poison_input.txt"
    assert os.path.exists(path), f"File {path} does not exist. You must create it."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "0", f"Expected poison input to be '0', but got '{content}'."

def test_fixed_server_code_exists():
    path = "/home/user/fixed_server.go"
    assert os.path.exists(path), f"Fixed server code {path} does not exist."

def test_server_running_and_normal_request():
    url = "http://localhost:8081/calculate"
    data = json.dumps({"number": 5}).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Expected HTTP 200 for valid input, got {response.status}."
    except urllib.error.HTTPError as e:
        pytest.fail(f"Server returned an error for a valid request: HTTP {e.code}")
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to the fixed server on port 8081. Is it running? Error: {e}")

def test_server_handles_poison_input():
    url = "http://localhost:8081/calculate"
    data = json.dumps({"number": 0}).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            pytest.fail(f"Service is still vulnerable! Expected HTTP 400 for poison input, but got HTTP {response.status}.")
    except urllib.error.HTTPError as e:
        assert e.code == 400, f"Expected HTTP 400 Bad Request for poison input, but got HTTP {e.code}."
    except urllib.error.URLError as e:
        if "timed out" in str(e.reason).lower() or isinstance(e.reason, TimeoutError):
            pytest.fail("Request timed out. The service is likely still stuck in an infinite loop allocating memory.")
        else:
            pytest.fail(f"Unexpected connection error when testing poison input: {e}")