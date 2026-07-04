# test_final_state.py

import os
import subprocess
import time
import json
import urllib.request
import urllib.error
import pytest

APP_DIR = "/home/user/app"

def test_stubs_generated():
    """Verify that the protocol buffer stubs have been compiled."""
    pb2_path = os.path.join(APP_DIR, "processor_pb2.py")
    pb2_grpc_path = os.path.join(APP_DIR, "processor_pb2_grpc.py")

    assert os.path.isfile(pb2_path), f"Stub file {pb2_path} is missing. Did you compile the proto file?"
    assert os.path.isfile(pb2_grpc_path), f"Stub file {pb2_grpc_path} is missing. Did you compile the proto file?"

def test_e2e_script():
    """Verify that the end-to-end script runs successfully and writes the correct log."""
    script_path = os.path.join(APP_DIR, "run_e2e.sh")
    log_path = os.path.join(APP_DIR, "test_results.log")

    assert os.path.isfile(script_path), f"E2E script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"E2E script {script_path} is not executable."

    # Remove existing log file to ensure we read the new one
    if os.path.exists(log_path):
        os.remove(log_path)

    # Run the E2E script
    result = subprocess.run([script_path], cwd=APP_DIR, capture_output=True, text=True)

    assert os.path.isfile(log_path), f"Log file {log_path} was not created by run_e2e.sh."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "E2E_ALL_PASS", f"Expected 'E2E_ALL_PASS' in {log_path}, but got: '{content}'"

def test_proxy_endpoints():
    """Verify that the proxy routes requests to the backend correctly."""
    proxy_path = os.path.join(APP_DIR, "proxy.py")
    backend_path = os.path.join(APP_DIR, "backend.py")

    assert os.path.isfile(proxy_path), f"Proxy script {proxy_path} is missing."

    # Start backend and proxy independently
    backend_proc = subprocess.Popen(["python3", backend_path], cwd=APP_DIR)
    proxy_proc = subprocess.Popen(["python3", proxy_path], cwd=APP_DIR)

    try:
        # Wait for services to become available
        time.sleep(3)

        # Test 'upper' action
        url_upper = "http://localhost:8080/api/v1/process/upper?text=verification"
        try:
            req = urllib.request.Request(url_upper)
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                assert data.get("result") == "VERIFICATION", f"Expected 'VERIFICATION' for upper action, got {data.get('result')}"
        except Exception as e:
            pytest.fail(f"Failed to request upper action at {url_upper}: {e}")

        # Test 'reverse' action
        url_reverse = "http://localhost:8080/api/v1/process/reverse?text=verification"
        try:
            req = urllib.request.Request(url_reverse)
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                assert data.get("result") == "noitacifirev", f"Expected 'noitacifirev' for reverse action, got {data.get('result')}"
        except Exception as e:
            pytest.fail(f"Failed to request reverse action at {url_reverse}: {e}")

        # Test invalid action (should return HTTP 400)
        url_invalid = "http://localhost:8080/api/v1/process/invalid?text=verification"
        try:
            req = urllib.request.Request(url_invalid)
            with urllib.request.urlopen(req, timeout=5) as response:
                pytest.fail(f"Expected HTTP 400 for invalid action, but got HTTP {response.status}")
        except urllib.error.HTTPError as e:
            assert e.code == 400, f"Expected HTTP 400 for invalid action, got HTTP {e.code}"
        except Exception as e:
            pytest.fail(f"Unexpected error when requesting invalid action at {url_invalid}: {e}")

    finally:
        # Gracefully terminate processes
        backend_proc.terminate()
        proxy_proc.terminate()
        backend_proc.wait()
        proxy_proc.wait()