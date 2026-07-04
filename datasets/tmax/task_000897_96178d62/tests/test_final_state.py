# test_final_state.py

import os
import socket
import struct
import subprocess
import requests
import pytest

def test_bad_commit_file():
    bad_commit_file = "/home/user/bad_commit.txt"
    assert os.path.isfile(bad_commit_file), f"File {bad_commit_file} does not exist."

    with open(bad_commit_file, "r") as f:
        sha = f.read().strip()

    assert len(sha) in (40, 7), f"Invalid Git SHA format in {bad_commit_file}: {sha}"

    repo_path = "/home/user/telemetry_server"

    # Verify the SHA exists in the repo
    try:
        subprocess.run(
            ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
            cwd=repo_path,
            check=True,
            capture_output=True
        )
    except subprocess.CalledProcessError:
        pytest.fail(f"The commit SHA {sha} found in {bad_commit_file} is not a valid commit in the repository.")

def test_http_health_check():
    try:
        response = requests.get("http://127.0.0.1:8080/health", timeout=2)
        assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
        data = response.json()
        assert data.get("status") == "ok", f"Expected {{'status': 'ok'}}, got {data}"
    except requests.RequestException as e:
        pytest.fail(f"HTTP health check failed: {e}")

def test_tcp_telemetry_protocol():
    host = "127.0.0.1"
    port = 9090

    try:
        with socket.create_connection((host, port), timeout=2) as s:
            # Send auth token
            auth_msg = b"AUTH_TOKEN: 8a9b4c2d-1234\n"
            s.sendall(auth_msg)

            # Create a malformed UTF-8 string payload
            # Valid ASCII 'hello', invalid byte \xff, valid ASCII 'world'
            payload = b"hello\xffworld"

            # The oracle expects a 4-byte length header followed by the string payload.
            # Assuming little-endian or network byte order (big-endian). Let's try little-endian first, 
            # or we can just send the length as a 32-bit integer. Usually network byte order is big-endian.
            # Let's send 4 bytes length in little-endian as it's common in C unless specified.
            # We'll use struct.pack to format it.
            header = struct.pack("<I", len(payload))

            s.sendall(header + payload)

            # Read response
            response = s.recv(1024)

            expected_response = b"ACK: hello?world"
            assert response == expected_response, f"Expected {expected_response}, got {response}"

    except (socket.error, socket.timeout) as e:
        pytest.fail(f"TCP telemetry protocol test failed: {e}")