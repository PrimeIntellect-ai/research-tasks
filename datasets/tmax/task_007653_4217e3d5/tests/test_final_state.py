# test_final_state.py

import os
import urllib.request
import subprocess

def test_libcalc_shared_object():
    """Verify libcalc.so is built as a valid shared object."""
    so_path = "/home/user/app/libcalc.so"
    assert os.path.isfile(so_path), f"{so_path} does not exist. Did you run make?"

    # Use 'file' command to check if it's a shared object
    result = subprocess.run(['file', so_path], capture_output=True, text=True)
    assert "shared object" in result.stdout, f"{so_path} is not a valid shared object. Check your Makefile."

def test_memory_leak_fixed():
    """Verify the memory leak in api.py is removed."""
    api_path = "/home/user/app/api.py"
    assert os.path.isfile(api_path), f"{api_path} does not exist."

    with open(api_path, 'r') as f:
        content = f.read()

    assert "history.append" not in content, "Memory leak (history.append) is still present in api.py."

def test_nginx_proxy_and_api_functional():
    """Verify Nginx reverse proxy works and returns correct result from API."""
    url = "http://127.0.0.1:8080/compute?val=10"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.getcode()
            body = response.read().decode('utf-8').strip()

            assert status == 200, f"Expected HTTP 200, got {status}"
            assert body == "20", f"Expected response body '20', got '{body}'"
    except Exception as e:
        assert False, f"Failed to connect to Nginx proxy or API: {e}"

def test_success_log():
    """Verify success log exists and has correct content."""
    log_path = "/home/user/app/success.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist. Did you run your test script?"

    with open(log_path, 'r') as f:
        content = f.read().strip()

    assert "Proxy and API functional" in content, f"Expected 'Proxy and API functional' in {log_path}, got '{content}'"

def test_test_script_exists():
    """Verify the test script was created."""
    test_path = "/home/user/app/test.py"
    assert os.path.isfile(test_path), f"{test_path} was not created."