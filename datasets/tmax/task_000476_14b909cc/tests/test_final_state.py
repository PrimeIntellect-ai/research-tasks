# test_final_state.py

import os
import socket
import pytest

def send_and_receive(host, port, message, timeout=3.0):
    """Helper function to send a message to a TCP server and return the response."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            s.sendall(message.encode('utf-8'))
            response = s.recv(1024).decode('utf-8')
            return response
    except ConnectionRefusedError:
        pytest.fail(f"Connection refused to {host}:{port}. The server is not running or listening.")
    except socket.timeout:
        pytest.fail(f"Connection or read timed out on {host}:{port} after {timeout} seconds.")
    except Exception as e:
        pytest.fail(f"Unexpected network error: {e}")

def test_c_source_exists_and_uses_seccomp():
    """Verify the C source code exists and implements seccomp process isolation."""
    source_path = "/home/user/secure_auth_server.c"
    assert os.path.isfile(source_path), f"Source file {source_path} is missing."

    with open(source_path, 'r') as f:
        content = f.read()

    # Check for indications of seccomp usage (either libseccomp or standard prctl)
    uses_seccomp = any(keyword in content for keyword in [
        "seccomp_init", 
        "seccomp_load", 
        "seccomp_rule_add",
        "PR_SET_SECCOMP", 
        "SECCOMP_MODE_STRICT", 
        "SECCOMP_MODE_FILTER"
    ])
    assert uses_seccomp, "Source code does not appear to implement seccomp process isolation (missing seccomp or prctl keywords)."

def test_tcp_server_granted():
    """Verify the server grants access for the correct recovered master token."""
    # The master token is "W4X9zk" (MD5: c4efd5020cb49b9d3257ffa0fbccc0ff)
    response = send_and_receive("127.0.0.1", 8888, "W4X9zk\n")
    assert response == "GRANTED\n", f"Expected 'GRANTED\\n' for correct token, but received {repr(response)}"

def test_tcp_server_denied_wrong_suffix():
    """Verify the server denies access for a token with the correct base but wrong suffix."""
    response = send_and_receive("127.0.0.1", 8888, "W4X9aa\n")
    assert response == "DENIED\n", f"Expected 'DENIED\\n' for incorrect token, but received {repr(response)}"

def test_tcp_server_denied_invalid_token():
    """Verify the server denies access for a completely invalid token."""
    response = send_and_receive("127.0.0.1", 8888, "invalid\n")
    assert response == "DENIED\n", f"Expected 'DENIED\\n' for invalid token, but received {repr(response)}"