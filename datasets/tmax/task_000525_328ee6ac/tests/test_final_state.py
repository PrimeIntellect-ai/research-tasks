# test_final_state.py
import socket
import requests
import os
import subprocess
import json

def test_http_versions_endpoint():
    try:
        response = requests.get("http://127.0.0.1:8080/versions", timeout=5)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        raise AssertionError(f"Failed to connect to HTTP server on port 8080 or invalid response: {e}")

    expected = {"python": "3.8", "node": "14", "go": "1.18"}
    assert data == expected, f"Expected {expected}, got {data}"

def test_tcp_build_endpoint():
    try:
        with socket.create_connection(("127.0.0.1", 9000), timeout=5) as sock:
            sock.sendall(b"BUILD\n")
            response = sock.recv(1024).decode("utf-8")
    except Exception as e:
        raise AssertionError(f"Failed to connect to TCP server on port 9000 or communicate: {e}")

    assert response == "SUCCESS\n", f"Expected 'SUCCESS\\n' from TCP server, got {repr(response)}"

def test_build_script_exists_and_executable():
    script_path = "/home/user/build.sh"
    assert os.path.isfile(script_path), f"Build script missing at {script_path}"
    assert os.access(script_path, os.X_OK), f"Build script at {script_path} is not executable"

    try:
        output = subprocess.check_output([script_path], text=True).strip()
    except subprocess.CalledProcessError as e:
        raise AssertionError(f"Build script failed with exit code {e.returncode}")

    expected_output = 'Building with Python 3.8, Node 14, Go 1.18'
    assert output == expected_output, f"Expected output {repr(expected_output)}, got {repr(output)}"