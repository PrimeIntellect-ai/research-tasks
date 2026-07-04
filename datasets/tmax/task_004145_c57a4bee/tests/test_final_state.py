# test_final_state.py

import os
import socket
import time
import pytest

HOST = '127.0.0.1'
PORT = 8080
LOG_FILE = '/home/user/audit.log'

def send_tcp_request(host, port, payload):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(3.0)
        s.connect((host, port))
        s.sendall(payload.encode('utf-8'))
        response = s.recv(1024).decode('utf-8')
    return response

def test_files_exist():
    """Verify that the C source and compiled binary exist."""
    assert os.path.exists('/home/user/audit_server.c'), "Source code /home/user/audit_server.c is missing."
    assert os.path.exists('/home/user/audit_server'), "Compiled binary /home/user/audit_server is missing."
    assert os.access('/home/user/audit_server', os.X_OK), "Compiled binary /home/user/audit_server is not executable."

def test_server_listening():
    """Verify that the server is listening on port 8080."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex((HOST, PORT))
        assert result == 0, f"Server is not listening on {HOST}:{PORT}"

def test_valid_auth_and_logging():
    """Verify that a valid token and payload result in SUCCESS and correct logging."""
    payload = "TOKEN: 7391 PAYLOAD: U2VjdXJlQXVkaXRMb2cxMjM=\n"
    try:
        response = send_tcp_request(HOST, PORT, payload)
    except Exception as e:
        pytest.fail(f"Failed to connect or receive response from server: {e}")

    assert response == "SUCCESS\n", f"Expected response 'SUCCESS\\n', got '{response}'"

    # Check the log file
    assert os.path.exists(LOG_FILE), f"Log file {LOG_FILE} was not created."
    with open(LOG_FILE, 'r') as f:
        lines = f.readlines()

    assert len(lines) > 0, f"Log file {LOG_FILE} is empty."
    assert "SecureAuditLog123" in lines[-1], f"Expected 'SecureAuditLog123' in the last line of {LOG_FILE}, got '{lines[-1]}'"

def test_invalid_auth():
    """Verify that an invalid token results in AUTH_FAILED."""
    payload = "TOKEN: 9999 PAYLOAD: YmFkX2FjdG9y\n"
    try:
        response = send_tcp_request(HOST, PORT, payload)
    except Exception as e:
        pytest.fail(f"Failed to connect or receive response from server: {e}")

    assert response == "AUTH_FAILED\n", f"Expected response 'AUTH_FAILED\\n', got '{response}'"

def test_buffer_overflow_attempt():
    """Verify that the server does not crash when sent a large payload."""
    large_payload_b64 = "A" * 2000
    payload = f"TOKEN: 7391 PAYLOAD: {large_payload_b64}\n"

    try:
        send_tcp_request(HOST, PORT, payload)
    except Exception:
        # It's okay if the connection drops or times out, as long as the server doesn't crash
        pass

    time.sleep(1) # Give the server a moment to potentially crash

    # Check if the server is still listening
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex((HOST, PORT))
        assert result == 0, "Server crashed after receiving a large payload (buffer overflow vulnerability)."