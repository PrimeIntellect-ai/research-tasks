# test_final_state.py
import os
import socket
import pytest

def test_binary_exists():
    """Verify that the compiled binary exists."""
    binary_path = "/home/user/metrics_server"
    assert os.path.isfile(binary_path), f"Compiled binary not found at {binary_path}. Did you compile the C code?"

def test_service_handles_overflow_payload():
    """Verify the service handles the oversized payload correctly."""
    payload = b"U3VwZXJMb25nQ29ycnVwdGVkUGF5bG9hZFRoYXRDcmFzaGVzVGhlU2VydmVy\n"

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3.0)
            s.connect(("127.0.0.1", 9090))
            s.sendall(payload)
            response = s.recv(1024)
    except ConnectionRefusedError:
        pytest.fail("Service is not listening on 127.0.0.1:9090")
    except socket.timeout:
        pytest.fail("Service timed out while handling the overflow payload")

    assert response.decode('utf-8') == "ERR: OVERFLOW\n", f"Expected 'ERR: OVERFLOW\\n', but got {response!r}"

def test_service_handles_valid_payload():
    """Verify the service handles a valid, short payload correctly."""
    payload = b"U2hvcnRQYXlsb2Fk\n"

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3.0)
            s.connect(("127.0.0.1", 9090))
            s.sendall(payload)
            response = s.recv(1024)
    except ConnectionRefusedError:
        pytest.fail("Service is not listening on 127.0.0.1:9090")
    except socket.timeout:
        pytest.fail("Service timed out while handling the valid payload")

    assert response.decode('utf-8') == "OK\n", f"Expected 'OK\\n', but got {response!r}"