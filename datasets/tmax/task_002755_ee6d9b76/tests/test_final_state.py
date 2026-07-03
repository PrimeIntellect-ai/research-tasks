# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error
import pytest

def test_make_success_and_binaries_exist():
    workspace = "/home/user/protocol_backend"

    # Check if binaries exist
    lib_path = os.path.join(workspace, "libproto.so")
    server_path = os.path.join(workspace, "server")

    assert os.path.isfile(lib_path), f"Shared library {lib_path} does not exist. Did make succeed?"
    assert os.path.isfile(server_path), f"Server binary {server_path} does not exist. Did make succeed?"

    # Run make clean and make to ensure it builds without error
    subprocess.run(["make", "clean"], cwd=workspace, capture_output=True)
    result = subprocess.run(["make"], cwd=workspace, capture_output=True, text=True)

    assert result.returncode == 0, f"make failed with error:\n{result.stderr}"
    assert "multiple definition" not in result.stderr, "Linking error 'multiple definition' still present."

def test_nginx_proxy_works():
    # Send a request to localhost:8080 to see if it proxies to the backend
    # The backend should echo the body back.
    test_string = b"pytest_proxy_test_string_123"
    req = urllib.request.Request("http://127.0.0.1:8080/", data=test_string, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            body = response.read()
            assert body == test_string, f"Expected response {test_string}, but got {body}. Proxy or backend is not working correctly."
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx on port 8080: {e}")

def test_prop_test_script():
    script_path = "/home/user/protocol_backend/prop_test.sh"

    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Run the script
    result = subprocess.run([script_path], capture_output=True, text=True)

    assert result.returncode == 0, f"prop_test.sh failed with exit code {result.returncode}.\nOutput: {result.stdout}\nError: {result.stderr}"
    assert "PASS: ALL" in result.stdout, f"prop_test.sh did not print 'PASS: ALL'.\nOutput: {result.stdout}"