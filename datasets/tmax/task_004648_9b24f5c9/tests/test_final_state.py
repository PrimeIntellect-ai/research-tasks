# test_final_state.py

import os
import base64
import socket
import requests
import pytest

def test_secscanner_setup_fixed():
    setup_path = "/app/secscanner-1.0.4/setup.py"
    assert os.path.isfile(setup_path), f"File {setup_path} does not exist."
    with open(setup_path, "r") as f:
        content = f.read()
    assert "baddep==9.9.9" not in content, "The invalid dependency 'baddep==9.9.9' was not removed from setup.py."

def test_secscanner_redactor_fixed():
    redactor_path = "/app/secscanner-1.0.4/secscanner/redactor.py"
    assert os.path.isfile(redactor_path), f"File {redactor_path} does not exist."
    with open(redactor_path, "r") as f:
        content = f.read()
    assert "b32decode" not in content, "The base64 decoding still uses 'b32decode'."
    assert "b64decode" in content, "The base64 decoding was not changed to 'b64decode'."

def test_http_endpoint_world_readable_file():
    test_file = "/tmp/test_config_644.json"
    with open(test_file, "w") as f:
        f.write("dummy")
    os.chmod(test_file, 0o644)

    payload = {
        "filepath": test_file,
        "encoded_payload": base64.b64encode(b"secret AKIAABCDEFGHIJKLMNOP").decode("utf-8")
    }

    try:
        response = requests.post("http://127.0.0.1:8080/scan", json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP request to /scan failed: {e}")

    assert response.status_code == 403, f"Expected HTTP 403 for world-readable file, got {response.status_code}. Response: {response.text}"

def test_http_endpoint_strict_file():
    test_file = "/tmp/test_config_600.json"
    with open(test_file, "w") as f:
        f.write("dummy")
    os.chmod(test_file, 0o600)

    raw_payload = b"user_data: AKIA0123456789ABCDEF, other_data: test"
    payload = {
        "filepath": test_file,
        "encoded_payload": base64.b64encode(raw_payload).decode("utf-8")
    }

    try:
        response = requests.post("http://127.0.0.1:8080/scan", json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP request to /scan failed: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for strict file, got {response.status_code}. Response: {response.text}"

    with open(test_file, "r") as f:
        written_content = f.read()

    assert "AKIA0123456789ABCDEF" not in written_content, "The sensitive API key was not redacted."
    assert "[REDACTED]" in written_content, "The redacted placeholder '[REDACTED]' was not found in the output."
    assert written_content == "user_data: [REDACTED], other_data: test", f"Unexpected file content: {written_content}"

def test_grpc_port_open():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect(("127.0.0.1", 50051))
        s.close()
    except Exception as e:
        pytest.fail(f"gRPC port 50051 is not open or reachable: {e}")