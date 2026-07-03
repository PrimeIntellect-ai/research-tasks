# test_final_state.py

import os
import socket
import pytest

def test_vuln_dir_txt():
    """Verify that the hardcoded upload directory was correctly extracted."""
    path = "/app/vuln_dir.txt"
    assert os.path.isfile(path), f"Missing required file: {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "/var/www/internal_uploads/"
    assert content == expected, f"Expected '{expected}' in {path}, but found '{content}'"

def test_clean_logs_txt():
    """Verify that the compromised logs were properly redacted."""
    path = "/app/clean_logs.txt"
    assert os.path.isfile(path), f"Missing required file: {path}"

    with open(path, "r") as f:
        content = f.read()

    expected = """GET /admin HTTP/1.1
Host: internal.corp
Cookie: session_token=[REDACTED]
User-Agent: Mozilla/5.0

GET /upload HTTP/1.1
Host: internal.corp
Cookie: session_token=[REDACTED]
User-Agent: curl/7.68.0
"""
    assert content.strip() == expected.strip(), "The redacted logs do not match the expected output."

def send_raw_http_request(host, port, request_str):
    """Helper to send raw HTTP requests to avoid URL normalization by HTTP clients."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2.0)
        try:
            s.connect((host, port))
        except ConnectionRefusedError:
            pytest.fail(f"Could not connect to honeypot service at {host}:{port}. Is it running?")

        s.sendall(request_str.encode('utf-8'))

        response = b""
        try:
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response += chunk
        except socket.timeout:
            # Expected if the server doesn't close the connection
            pass

    return response.decode('utf-8', errors='replace')

def test_honeypot_logs_endpoint():
    """Verify the honeypot responds to GET /logs with the clean logs."""
    request = "GET /logs HTTP/1.1\r\nHost: 127.0.0.1:8443\r\n\r\n"
    response = send_raw_http_request("127.0.0.1", 8443, request)

    assert "HTTP/1.1 200 OK" in response, f"Expected HTTP 200 OK, got:\n{response}"
    assert "X-Incident-Response: Active" in response, f"Missing required header 'X-Incident-Response: Active' in response:\n{response}"

    # Verify the body contains the redacted logs
    with open("/app/clean_logs.txt", "r") as f:
        expected_body = f.read().strip()

    assert expected_body in response, "Response body does not contain the expected clean logs."

def test_honeypot_path_traversal():
    """Verify the honeypot blocks path traversal attempts."""
    request = "GET /logs/../../etc/passwd HTTP/1.1\r\nHost: 127.0.0.1:8443\r\n\r\n"
    response = send_raw_http_request("127.0.0.1", 8443, request)

    assert "HTTP/1.1 403 Forbidden" in response, f"Expected HTTP 403 Forbidden for path traversal, got:\n{response}"
    assert "X-Incident-Response: Active" in response, f"Missing required header 'X-Incident-Response: Active' in response:\n{response}"

def test_honeypot_not_found():
    """Verify the honeypot returns 404 for unknown paths."""
    request = "GET /random HTTP/1.1\r\nHost: 127.0.0.1:8443\r\n\r\n"
    response = send_raw_http_request("127.0.0.1", 8443, request)

    assert "HTTP/1.1 404 Not Found" in response, f"Expected HTTP 404 Not Found for unknown path, got:\n{response}"
    assert "X-Incident-Response: Active" in response, f"Missing required header 'X-Incident-Response: Active' in response:\n{response}"