# test_final_state.py

import os
import socket
import pytest
import requests

def test_source_code_exists():
    """Verify that the Go source code was saved at the correct location."""
    file_path = "/home/user/pipeline.go"
    assert os.path.exists(file_path), f"Expected Go source code at {file_path} does not exist."
    assert os.path.isfile(file_path), f"Expected {file_path} to be a file."

def test_http_server_valid_request():
    """Verify the HTTP server responds correctly to a valid request."""
    url = "http://127.0.0.1:8080/sequence"
    headers = {"Authorization": "Bearer bio-perf-token"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP request to {url} failed: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"
    expected_body = ">Extracted_Sequence\nAGCTA"
    assert response.text.strip() == expected_body, f"Expected response body '{expected_body}', got '{response.text.strip()}'"

def test_http_server_invalid_request():
    """Verify the HTTP server responds with 401 for an invalid token."""
    url = "http://127.0.0.1:8080/sequence"
    headers = {"Authorization": "Bearer invalid-token"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP request to {url} failed: {e}")

    assert response.status_code in (401, 404), f"Expected HTTP 401 or 404 for invalid token, got {response.status_code}"

def test_tcp_server_response():
    """Verify the TCP server responds correctly to the PING command."""
    host = "127.0.0.1"
    port = 9090
    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            sock.sendall(b"PING\n")
            data = sock.recv(4096)
    except Exception as e:
        pytest.fail(f"TCP connection or communication with {host}:{port} failed: {e}")

    response_text = data.decode('utf-8')
    expected_response = ">Extracted_Sequence\nAGCTA\n"

    # We strip trailing whitespace to be forgiving about exact newline characters, 
    # but ensure the core content matches.
    assert response_text.strip() == expected_response.strip(), f"Expected TCP response '{expected_response.strip()}', got '{response_text.strip()}'"