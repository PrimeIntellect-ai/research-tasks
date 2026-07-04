# test_final_state.py
import socket
import pytest

def send_raw_request(req_str):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3.0)
    try:
        s.connect(('127.0.0.1', 8080))
        s.sendall(req_str.encode('utf-8'))
        resp = b""
        while True:
            try:
                chunk = s.recv(4096)
                if not chunk:
                    break
                resp += chunk
            except socket.timeout:
                break
        return resp.decode('utf-8', errors='replace')
    finally:
        s.close()

def test_gateway_alg_none_lowercase():
    req = (
        "GET / HTTP/1.1\r\n"
        "Host: 127.0.0.1:8080\r\n"
        "Authorization: Bearer eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyIjoiYWRtaW4ifQ.\r\n"
        "\r\n"
    )
    resp = send_raw_request(req)
    assert "HTTP/1.1 403 Forbidden" in resp, f"Expected 403 Forbidden, got: {resp}"
    assert "Policy Violation\n" in resp, f"Expected 'Policy Violation\\n' in body, got: {resp}"

def test_gateway_alg_none_uppercase():
    req = (
        "GET / HTTP/1.1\r\n"
        "Host: 127.0.0.1:8080\r\n"
        "Authorization: Bearer eyJhbGciOiJOT05FIiwidHlwIjoiSldUIn0.eyJ1c2VyIjoiYWRtaW4ifQ.\r\n"
        "\r\n"
    )
    resp = send_raw_request(req)
    assert "HTTP/1.1 403 Forbidden" in resp, f"Expected 403 Forbidden, got: {resp}"
    assert "Policy Violation\n" in resp, f"Expected 'Policy Violation\\n' in body, got: {resp}"

def test_gateway_alg_valid_hs256():
    req = (
        "GET / HTTP/1.1\r\n"
        "Host: 127.0.0.1:8080\r\n"
        "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidXNlcjEifQ.signature\r\n"
        "\r\n"
    )
    resp = send_raw_request(req)
    assert "HTTP/1.1 200 OK" in resp, f"Expected 200 OK, got: {resp}"
    assert "X-Policy-ID: 77DF" in resp, f"Expected X-Policy-ID: 77DF header, got: {resp}"
    assert "Access Granted\n" in resp, f"Expected 'Access Granted\\n' in body, got: {resp}"