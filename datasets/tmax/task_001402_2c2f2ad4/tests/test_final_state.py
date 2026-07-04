# test_final_state.py

import os
import socket
import stat
import pytest
import subprocess

PORT = 8090
ENDPOINT = "/ping"
AUTH_KEY = "vnc_alert_trigger_77"

def test_c_source_exists():
    """Verify that the C source code exists."""
    path = "/home/user/monitor.c"
    assert os.path.exists(path), f"C source file {path} is missing."
    assert os.path.isfile(path), f"{path} is not a file."

def test_compiled_binary_exists():
    """Verify that the compiled binary exists and is executable."""
    path = "/home/user/monitor_service"
    assert os.path.exists(path), f"Compiled binary {path} is missing."
    assert os.path.isfile(path), f"{path} is not a file."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{path} is not executable."

def test_manage_script_exists():
    """Verify that the management bash script exists and is executable."""
    path = "/home/user/manage_service.sh"
    assert os.path.exists(path), f"Bash script {path} is missing."
    assert os.path.isfile(path), f"{path} is not a file."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{path} is not executable."

def test_service_valid_endpoint():
    """Verify that the service responds correctly to the valid endpoint."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3.0)
    try:
        s.connect(("127.0.0.1", PORT))
        request = f"GET {ENDPOINT} HTTP/1.0\r\nHost: 127.0.0.1\r\n\r\n"
        s.sendall(request.encode('utf-8'))
        response_bytes = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response_bytes += chunk
    except ConnectionRefusedError:
        pytest.fail(f"Connection refused on port {PORT}. Is the service running?")
    except socket.timeout:
        pytest.fail("Connection timed out while waiting for response.")
    finally:
        s.close()

    response = response_bytes.decode('utf-8', errors='ignore')
    assert response, "Received empty response from the server."

    lines = response.replace('\r\n', '\n').split('\n')
    status_line = lines[0]
    assert "200" in status_line, f"Expected 200 OK status, got: {status_line}"

    # Check if the auth key is in the body
    assert AUTH_KEY in response, f"Expected AUTH_KEY '{AUTH_KEY}' not found in response."

def test_service_invalid_endpoint():
    """Verify that the service responds with 404 to an invalid endpoint."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3.0)
    try:
        s.connect(("127.0.0.1", PORT))
        request = "GET /invalid_path_123 HTTP/1.0\r\nHost: 127.0.0.1\r\n\r\n"
        s.sendall(request.encode('utf-8'))
        response_bytes = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response_bytes += chunk
    except ConnectionRefusedError:
        pytest.fail(f"Connection refused on port {PORT}. Is the service running?")
    except socket.timeout:
        pytest.fail("Connection timed out while waiting for response.")
    finally:
        s.close()

    response = response_bytes.decode('utf-8', errors='ignore')
    assert response, "Received empty response from the server."

    lines = response.replace('\r\n', '\n').split('\n')
    status_line = lines[0]
    assert "404" in status_line, f"Expected 404 Not Found status, got: {status_line}"