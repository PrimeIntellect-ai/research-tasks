# test_final_state.py
import os
import json
import urllib.request
import urllib.error
import ctypes

def test_makefile_and_shared_library():
    so_path = "/home/user/legacy_app/libprocessor.so"
    assert os.path.isfile(so_path), "libprocessor.so was not built."

    # Check if it's a valid shared library that can be loaded
    try:
        lib = ctypes.CDLL(so_path)
    except Exception as e:
        assert False, f"Failed to load libprocessor.so as a shared library: {e}. Make sure the Makefile uses -shared and -fPIC."

    # Check if process_string is accessible
    assert hasattr(lib, "process_string"), "process_string symbol not found in libprocessor.so."

def test_api_pid_file():
    pid_file = "/home/user/api.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} is missing."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), "PID file does not contain a valid integer."
    pid = int(pid_str)

    # Check if process is running
    try:
        os.kill(pid, 0)
    except OSError:
        assert False, f"Process with PID {pid} is not running."

def test_rest_api_endpoint():
    # Test the API endpoint
    url = "http://127.0.0.1:8000/api/transform?text=Python2to3"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            status = response.getcode()
            content_type = response.headers.get("Content-Type", "")
            data = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to API or API returned an error: {e}"

    assert status == 200, f"Expected HTTP 200, got {status}"
    assert "application/json" in content_type, f"Expected Content-Type application/json, got {content_type}"

    try:
        json_data = json.loads(data)
    except json.JSONDecodeError:
        assert False, f"API response is not valid JSON: {data}"

    assert "result" in json_data, "JSON response is missing 'result' key."
    assert json_data["result"] == "Clguba2gb3", f"Expected transformed string 'Clguba2gb3', got {json_data['result']}"