# test_final_state.py

import os
import subprocess
import time
import urllib.request
import urllib.error
import json
import pytest

def test_rust_lib_built():
    so_path = "/home/user/rust_lib/target/release/librust_lib.so"
    assert os.path.isfile(so_path), f"Rust shared library not found at {so_path}. Did you build in release mode?"

def test_go_server_built():
    server_path = "/home/user/go_app/server"
    assert os.path.isfile(server_path), f"Go server binary not found at {server_path}."

def test_go_tests_pass():
    test_file = "/home/user/go_app/main_test.go"
    assert os.path.isfile(test_file), f"Go tests file not found at {test_file}."

    result = subprocess.run(
        ["go", "test", "-v"], 
        cwd="/home/user/go_app", 
        capture_output=True, 
        text=True
    )
    assert result.returncode == 0, f"Go tests failed. Output:\n{result.stdout}\n{result.stderr}"

@pytest.fixture(scope="module")
def go_server():
    server_path = "/home/user/go_app/server"
    if not os.path.isfile(server_path):
        pytest.fail("Server binary not found, cannot start server tests.")

    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = "/home/user/rust_lib/target/release:" + env.get("LD_LIBRARY_PATH", "")

    # Start the server
    proc = subprocess.Popen(
        [server_path], 
        cwd="/home/user/go_app", 
        env=env, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )

    # Give the server a moment to start
    time.sleep(2)

    # Check if process crashed immediately
    if proc.poll() is not None:
        stdout, stderr = proc.communicate()
        pytest.fail(f"Server crashed immediately. Stdout: {stdout}, Stderr: {stderr}")

    yield

    proc.terminate()
    try:
        proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()

def test_server_valid_math(go_server):
    req = urllib.request.Request("http://localhost:8080/compute", method="POST")
    req.add_header("Content-Type", "application/json")
    data = json.dumps({"coeffs": [2.0, 3.0], "x": 4.0}).encode("utf-8")

    try:
        with urllib.request.urlopen(req, data=data, timeout=2) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            resp_data = json.loads(response.read().decode("utf-8"))
            assert "result" in resp_data, "Response missing 'result' field"
            assert abs(resp_data["result"] - 11.0) < 1e-6, f"Expected result 11.0, got {resp_data['result']}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Request failed with HTTP {e.code}")
    except urllib.error.URLError as e:
        pytest.fail(f"Request failed: {e}")

def test_server_validation_400(go_server):
    req = urllib.request.Request("http://localhost:8080/compute", method="POST")
    req.add_header("Content-Type", "application/json")
    data = json.dumps({"coeffs": [], "x": 4.0}).encode("utf-8")

    try:
        urllib.request.urlopen(req, data=data, timeout=2)
        pytest.fail("Expected HTTP 400 for empty coeffs, but request succeeded")
    except urllib.error.HTTPError as e:
        assert e.code == 400, f"Expected HTTP 400, got {e.code}"
    except urllib.error.URLError as e:
        pytest.fail(f"Request failed: {e}")

def test_server_rate_limiting_429(go_server):
    # Wait to ensure we have a fresh rate limit window
    time.sleep(1.5)

    req = urllib.request.Request("http://localhost:8080/compute", method="POST")
    req.add_header("Content-Type", "application/json")
    data = json.dumps({"coeffs": [1.0], "x": 1.0}).encode("utf-8")

    status_codes = []
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, data=data, timeout=2) as response:
                status_codes.append(response.status)
        except urllib.error.HTTPError as e:
            status_codes.append(e.code)
        except urllib.error.URLError as e:
            pytest.fail(f"Request failed: {e}")

    assert 429 in status_codes, f"Expected at least one HTTP 429 Too Many Requests in 3 rapid requests, got statuses: {status_codes}"