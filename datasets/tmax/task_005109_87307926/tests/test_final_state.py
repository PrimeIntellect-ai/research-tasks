# test_final_state.py

import os
import subprocess
import time
import json
import urllib.request
import urllib.error
import pytest

PROJECT_DIR = "/home/user/project"
PATCH_FILE = os.path.join(PROJECT_DIR, "parser_fix.patch")
RUST_BINARY = os.path.join(PROJECT_DIR, "target", "debug", "rust_processor")
GATEWAY_PY = os.path.join(PROJECT_DIR, "gateway.py")

def test_patch_file_exists():
    assert os.path.isfile(PATCH_FILE), f"Patch file {PATCH_FILE} is missing."

def test_cargo_build_succeeds():
    result = subprocess.run(
        ["cargo", "build"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"cargo build failed:\n{result.stderr}"
    assert os.path.isfile(RUST_BINARY), f"Rust binary {RUST_BINARY} was not created."

def test_rust_binary_truncates_without_segfault():
    # A string longer than 15 characters (buffer is 16 bytes including null)
    long_input = "A" * 30
    result = subprocess.run(
        [RUST_BINARY, long_input],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Rust binary crashed (likely segfault) on long input."

    output = result.stdout.strip()
    assert len(output) <= 15, f"Output was not properly truncated. Length: {len(output)}"
    assert output == "A" * len(output), "Output content is corrupted."

def test_python_gateway_validation_and_rate_limiting():
    # Start the server in the background
    server_process = subprocess.Popen(
        ["python3", GATEWAY_PY],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Give the server a moment to start
    time.sleep(1)

    try:
        assert server_process.poll() is None, "Python gateway failed to start or crashed immediately."

        url = "http://127.0.0.1:8080"

        def send_request(payload):
            req = urllib.request.Request(
                url, 
                data=json.dumps(payload).encode('utf-8') if payload is not None else b"not json",
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            try:
                with urllib.request.urlopen(req) as response:
                    return response.status
            except urllib.error.HTTPError as e:
                return e.code
            except Exception as e:
                return None

        # Test malformed JSON
        status = send_request(None)
        assert status == 400, f"Expected 400 for malformed JSON, got {status}"

        # Test missing keys
        status = send_request({"data": "test"})
        assert status == 400, f"Expected 400 for missing user_id, got {status}"

        status = send_request({"user_id": "user1"})
        assert status == 400, f"Expected 400 for missing data, got {status}"

        # Test rate limiting
        user_id = "test_user_123"
        payload = {"user_id": user_id, "data": "hello"}

        # Requests 1 to 3 should be 200 OK
        for i in range(3):
            status = send_request(payload)
            assert status == 200, f"Expected 200 for request {i+1}, got {status}"

        # Request 4 should be 429 Too Many Requests
        status = send_request(payload)
        assert status == 429, f"Expected 429 for request 4, got {status}"

        # Another user should still be able to make requests
        status = send_request({"user_id": "another_user", "data": "hello"})
        assert status == 200, f"Expected 200 for a different user, got {status}"

    finally:
        server_process.terminate()
        server_process.wait(timeout=2)