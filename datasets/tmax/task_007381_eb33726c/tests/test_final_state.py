# test_final_state.py
import os
import subprocess
import time
import urllib.request
import urllib.error
import pytest

def test_binary_exists_and_executable():
    binary_path = "/home/user/release/math-api"
    assert os.path.isfile(binary_path), f"Release binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"File at {binary_path} is not executable"

def test_go_test_passes():
    workspace_dir = "/home/user/workspace"
    result = subprocess.run(["go", "test"], cwd=workspace_dir, capture_output=True, text=True)
    assert result.returncode == 0, f"'go test' failed. Output:\n{result.stdout}\n{result.stderr}"

def test_api_routing_and_logic():
    binary_path = "/home/user/release/math-api"

    # Start the binary in the background
    process = subprocess.Popen([binary_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        # Give the server a moment to start
        time.sleep(1)

        # Test the endpoint with negative and positive numbers
        url = "http://localhost:8080/gcd/-21/14"
        req = urllib.request.Request(url, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=2) as response:
                status = response.status
                body = response.read().decode('utf-8').strip()
        except urllib.error.HTTPError as e:
            pytest.fail(f"HTTP error {e.code} when accessing {url}")
        except urllib.error.URLError as e:
            pytest.fail(f"Failed to connect to the API: {e}")

        assert status == 200, f"Expected status 200, got {status}"
        assert body == "7", f"Expected GCD 7 for inputs -21 and 14, got '{body}'"

        # Test another endpoint with two positive numbers
        url2 = "http://localhost:8080/gcd/48/18"
        req2 = urllib.request.Request(url2, method="GET")
        try:
            with urllib.request.urlopen(req2, timeout=2) as response2:
                body2 = response2.read().decode('utf-8').strip()
        except urllib.error.URLError as e:
            pytest.fail(f"Failed to connect to the API: {e}")

        assert body2 == "6", f"Expected GCD 6 for inputs 48 and 18, got '{body2}'"

    finally:
        # Ensure the process is cleanly terminated
        process.terminate()
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()