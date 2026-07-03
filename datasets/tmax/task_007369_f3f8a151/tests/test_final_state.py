# test_final_state.py
import os
import socket
import time
import pytest

def send_request(path):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect(('127.0.0.1', 8080))
        req = f"GET {path} HTTP/1.1\r\nHost: localhost\r\n\r\n"
        s.sendall(req.encode())
        resp = s.recv(4096).decode()
        s.close()
        return resp
    except Exception as e:
        return str(e)

def test_server_compiled_and_running():
    """Verify that the server is compiled and running on port 8080."""
    assert os.path.isfile("/home/user/server"), "Server executable /home/user/server not found. Did you compile it?"
    assert os.access("/home/user/server", os.X_OK), "Server executable is not executable."

    # Check if port 8080 is open
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    result = s.connect_ex(('127.0.0.1', 8080))
    s.close()
    assert result == 0, "Server is not listening on port 8080. Did you run it in the background?"

def test_open_redirect_mitigation_invalid():
    """Verify that invalid redirect targets default to /dashboard."""
    resp = send_request("/login?redirect=http://evil.com")
    assert "Location: /dashboard\r\n" in resp, "Invalid redirect did not default to /dashboard."

def test_open_redirect_mitigation_valid():
    """Verify that valid redirect targets (/profile, /dashboard) are allowed."""
    resp = send_request("/login?redirect=/profile/settings")
    assert "Location: /profile/settings\r\n" in resp, "Valid redirect to /profile was altered or blocked."

def test_csp_header_presence():
    """Verify that the Content-Security-Policy header is included in 200 OK responses."""
    resp = send_request("/index.html")
    assert "Content-Security-Policy: default-src 'self'" in resp, "CSP header missing or incorrect in 200 OK response."

def test_sensitive_data_redaction():
    """Verify that the token parameter is redacted in the access log."""
    send_request("/api?user=1&token=SUPERSECRET&action=view")
    time.sleep(0.5)  # Wait for the log to be written

    log_path = "/home/user/access.log"
    assert os.path.isfile(log_path), "access.log not found. The server did not create the log file."

    with open(log_path, "r") as f:
        log_contents = f.read()

    assert "token=REDACTED&action=view" in log_contents, "Token was not correctly redacted in the log."
    assert "SUPERSECRET" not in log_contents, "Token secret leaked in the log file."