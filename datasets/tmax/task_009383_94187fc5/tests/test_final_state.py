# test_final_state.py
import os
import json
import urllib.request
import subprocess

WORKSPACE_DIR = "/home/user/workspace"

def test_libvm_so_compiled_correctly():
    lib_path = os.path.join(WORKSPACE_DIR, "libvm.so")
    assert os.path.isfile(lib_path), "libvm.so was not compiled"

    # Check if it's a shared object
    result = subprocess.run(["file", lib_path], capture_output=True, text=True)
    assert "shared object" in result.stdout.lower(), "libvm.so is not a valid shared object. Did you add -shared and -fPIC to the Makefile?"

def test_app_py_exists_and_uses_ctypes():
    app_path = os.path.join(WORKSPACE_DIR, "app.py")
    assert os.path.isfile(app_path), "app.py is missing"

    with open(app_path, "r") as f:
        content = f.read()

    assert "ctypes" in content, "app.py does not import/use ctypes"
    assert "libvm.so" in content, "app.py does not load libvm.so"

def test_test_app_py_exists():
    test_path = os.path.join(WORKSPACE_DIR, "test_app.py")
    assert os.path.isfile(test_path), "test_app.py is missing"

    with open(test_path, "r") as f:
        content = f.read()

    assert "TestClient" in content, "test_app.py does not use TestClient"
    assert "ADD 5" in content and "ADD 10" in content, "test_app.py does not contain the required test payload"

def test_api_endpoint_running_and_correct():
    url = "http://localhost:8000/api/v1/execute"
    payload = json.dumps({"program": "ADD 20\nSUB 5\nRET"}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.getcode()
            body = response.read().decode("utf-8")
            data = json.loads(body)
    except Exception as e:
        assert False, f"Failed to reach the API endpoint at {url} or bad response: {e}"

    assert status == 200, f"Expected HTTP 200, got {status}"
    assert "result" in data, "Response JSON missing 'result' key"
    assert data["result"] == 15, f"Expected result 15, got {data['result']}"

def test_success_log_exists():
    log_path = os.path.join(WORKSPACE_DIR, "success.log")
    assert os.path.isfile(log_path), "success.log is missing"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert "200" in content, f"success.log does not contain '200'. Found: '{content}'"