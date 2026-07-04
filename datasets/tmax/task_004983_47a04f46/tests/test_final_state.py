# test_final_state.py

import os
import pytest
import urllib.request

def test_libvm_so_exists():
    """Test that the shared library was built."""
    so_path = "/home/user/libvm.so"
    assert os.path.isfile(so_path), f"Shared library missing: {so_path}. Did you run make?"

def test_result_log_content():
    """Test that the result.log contains the correct output from the API."""
    log_path = "/home/user/result.log"
    assert os.path.isfile(log_path), f"Log file missing: {log_path}. Did you make the curl request and save the output?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "9", f"Expected result.log to contain '9', but found '{content}'"

def test_api_server_running_and_fixed():
    """Test that the API server is running and the FFI bug is fixed."""
    # We can try to hit the API to verify it is running and fixed.
    # If the server was stopped, this might fail, but the prompt says "Start the API server on port 8080 in the background."
    # We will test a different code to ensure it's not hardcoded.
    url = "http://127.0.0.1:8080/eval?code=P5M2P1"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            status = response.getcode()
            body = response.read().decode('utf-8').strip()
    except Exception as e:
        pytest.fail(f"Failed to reach API server at {url} or server crashed: {e}")

    assert status == 200, f"Expected HTTP 200 OK, got {status}"
    assert body == "4", f"Expected API to return '4' for P5M2P1, got '{body}'"