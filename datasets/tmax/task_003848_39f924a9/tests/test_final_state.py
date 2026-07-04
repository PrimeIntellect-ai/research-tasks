# test_final_state.py
import socket
import urllib.request
import urllib.error
import time
import os
import pytest

def adler32(data: str) -> int:
    a = 1
    b = 0
    for char in data:
        c = ord(char)
        a = (a + c) % 65521
        b = (b + a) % 65521
    return (b << 16) | a

def is_port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(('127.0.0.1', port)) == 0

def send_request(uri: str, checksum: str = None):
    req = urllib.request.Request(f"http://127.0.0.1:8080{uri}")
    if checksum is not None:
        req.add_header("X-Secure-Checksum", checksum)
    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            return response.status, response.read().decode('utf-8', errors='ignore')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return 0, str(e)

def test_ports_listening():
    assert is_port_open(9090), "Mock backend is not listening on port 9090."
    assert is_port_open(8080), "Security proxy is not listening on port 8080."

def test_proxy_missing_checksum():
    status, body = send_request("/test")
    assert status == 403, f"Expected 403 Forbidden for missing checksum, got {status}."

def test_proxy_valid_checksum():
    uri = "/api/data"
    checksum = str(adler32(uri))
    status, body = send_request(uri, checksum)
    assert status == 200, f"Expected 200 OK for valid checksum, got {status}."
    assert "Authorized Backend Data" in body, "Response body did not match expected backend data."

def test_proxy_invalid_checksum():
    uri = "/api/data"
    status, body = send_request(uri, "12345")
    assert status == 403, f"Expected 403 Forbidden for invalid checksum, got {status}."

def test_proxy_log_contents():
    log_path = "/home/user/proxy.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."

    time.sleep(0.5) # Allow some time for async writes if any
    with open(log_path, 'r') as f:
        logs = f.read()

    expected_lines = [
        "[DENY] /test NONE",
        f"[ALLOW] /api/data {adler32('/api/data')}",
        "[DENY] /api/data 12345"
    ]

    for line in expected_lines:
        assert line in logs, f"Expected log line '{line}' not found in {log_path}."