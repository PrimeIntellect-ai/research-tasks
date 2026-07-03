# test_final_state.py

import os
import subprocess
import time
import urllib.request
import urllib.error
import json
import pytest

def test_success_log_exists():
    assert os.path.isfile("/home/user/test_success.log"), "/home/user/test_success.log was not created. Did the Go tests pass?"

def test_source_files_exist():
    assert os.path.isfile("/home/user/src/main.go"), "/home/user/src/main.go is missing."
    assert os.path.isfile("/home/user/src/main_test.go"), "/home/user/src/main_test.go is missing."
    assert os.path.isfile("/home/user/Makefile"), "/home/user/Makefile is missing."

def test_makefile_builds_successfully():
    # Test make clean
    subprocess.run(["make", "clean"], cwd="/home/user", check=False)
    assert not os.path.exists("/home/user/bin/server"), "'make clean' did not remove /home/user/bin/server"
    assert not os.path.exists("/home/user/lib/libfilter.so"), "'make clean' did not remove /home/user/lib/libfilter.so"

    # Test make build
    result = subprocess.run(["make", "build"], cwd="/home/user", capture_output=True, text=True)
    assert result.returncode == 0, f"'make build' failed:\n{result.stderr}\n{result.stdout}"

    assert os.path.isfile("/home/user/bin/server"), "Server executable was not created at /home/user/bin/server"
    assert os.path.isfile("/home/user/lib/libfilter.so"), "Shared library was not created at /home/user/lib/libfilter.so"

@pytest.fixture(scope="module")
def running_server():
    # Ensure it's built
    subprocess.run(["make", "build"], cwd="/home/user", check=True)

    env = os.environ.copy()
    lib_path = "/home/user/lib"
    if "LD_LIBRARY_PATH" in env:
        env["LD_LIBRARY_PATH"] = f"{lib_path}:{env['LD_LIBRARY_PATH']}"
    else:
        env["LD_LIBRARY_PATH"] = lib_path

    process = subprocess.Popen(
        ["/home/user/bin/server"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for server to start
    time.sleep(2)

    yield "http://127.0.0.1:8080/api/action"

    process.terminate()
    process.wait()

def send_request(url, data, headers=None):
    if headers is None:
        headers = {}
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            return response.status
    except urllib.error.HTTPError as e:
        return e.code
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to server: {e}")

def test_server_403_forbidden(running_server):
    data = json.dumps({"user_id": "u1", "action": "jump"}).encode('utf-8')
    headers = {"X-Forwarded-For": "198.51.100.55", "Content-Type": "application/json"}
    status = send_request(running_server, data, headers)
    assert status == 403, f"Expected 403 Forbidden for blocked IP, got {status}"

def test_server_400_bad_request(running_server):
    # Missing user_id
    data = json.dumps({"action": "jump"}).encode('utf-8')
    headers = {"Content-Type": "application/json"}
    status = send_request(running_server, data, headers)
    assert status == 400, f"Expected 400 Bad Request for missing field, got {status}"

    # Invalid JSON
    data = b"not a json"
    status = send_request(running_server, data, headers)
    assert status == 400, f"Expected 400 Bad Request for invalid JSON, got {status}"

def test_server_200_and_429_rate_limit(running_server):
    data = json.dumps({"user_id": "u2", "action": "jump"}).encode('utf-8')
    headers = {"Content-Type": "application/json"}

    # First 3 requests should be 200 OK
    for i in range(3):
        status = send_request(running_server, data, headers)
        assert status == 200, f"Expected 200 OK for request {i+1}, got {status}"

    # 4th request should be 429 Too Many Requests
    status = send_request(running_server, data, headers)
    assert status == 429, f"Expected 429 Too Many Requests, got {status}"