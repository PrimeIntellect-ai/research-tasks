# test_final_state.py
import os
import socket
import pytest

def test_admin_token_extracted():
    token_path = '/home/user/admin_token.txt'
    assert os.path.isfile(token_path), f"{token_path} does not exist. The token was not extracted."
    with open(token_path, 'r') as f:
        token = f.read().strip()
    assert token == "WAF-SEC-99821", f"Extracted token is incorrect. Expected 'WAF-SEC-99821', got '{token}'."

def test_cmake_fixed():
    cmakelists_path = '/home/user/miniwaf/CMakeLists.txt'
    assert os.path.isfile(cmakelists_path), f"{cmakelists_path} is missing."
    with open(cmakelists_path, 'r') as f:
        content = f.read()
    assert 'target_link_libraries' in content, "CMakeLists.txt does not contain 'target_link_libraries'. The build is likely still broken."

def test_parser_memory_safety_fixed():
    parser_path = '/home/user/miniwaf/src/parser.c'
    assert os.path.isfile(parser_path), f"{parser_path} is missing."
    with open(parser_path, 'r') as f:
        content = f.read()
    # Ensure the unsafe strcpy is no longer used for the buffer
    assert 'strcpy(buffer, input_header);' not in content, "parser.c still contains the vulnerable 'strcpy' call."

def send_http_request(payload: str) -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    try:
        s.connect(('127.0.0.1', 8080))
        s.sendall(payload.encode('utf-8'))
        response = s.recv(4096).decode('utf-8', errors='ignore')
        return response
    finally:
        s.close()

def test_server_valid_request():
    req = "GET / HTTP/1.1\r\nHost: localhost\r\nAdmin-Token: WAF-SEC-99821\r\n\r\n"
    try:
        resp = send_http_request(req)
    except ConnectionRefusedError:
        pytest.fail("Connection refused to 127.0.0.1:8080. Is the server running?")
    assert "200 OK" in resp, f"Expected '200 OK' in response, got: {resp}"

def test_server_waf_blocking():
    req = "GET /?payload=<script>alert(1)</script> HTTP/1.1\r\nHost: localhost\r\n\r\n"
    try:
        resp = send_http_request(req)
    except ConnectionRefusedError:
        pytest.fail("Connection refused to 127.0.0.1:8080. Is the server running?")
    assert "403 Forbidden" in resp, f"Expected '403 Forbidden' in response, got: {resp}"

def test_server_memory_safety_long_header():
    long_header = "A" * 250
    req = f"GET / HTTP/1.1\r\nHost: localhost\r\nX-Custom-Header: {long_header}\r\n\r\n"
    try:
        resp = send_http_request(req)
    except ConnectionRefusedError:
        pytest.fail("Connection refused to 127.0.0.1:8080. Is the server running?")
    except (socket.timeout, ConnectionResetError):
        pytest.fail("Server crashed or dropped connection on long header! Memory safety bug is not fixed.")

    assert "200 OK" in resp or "400 Bad Request" in resp, f"Expected '200 OK' or '400 Bad Request' after long header, got: {resp}"