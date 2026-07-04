# test_final_state.py

import socket
import pytest

def send_and_receive(host, port, payload):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5.0)
        try:
            s.connect((host, port))
        except ConnectionRefusedError:
            pytest.fail(f"Connection refused to {host}:{port}. Ensure the service is running.")
        except Exception as e:
            pytest.fail(f"Failed to connect to {host}:{port}: {e}")

        s.sendall(payload.encode('utf-8'))

        data = b""
        while True:
            try:
                chunk = s.recv(1024)
                if not chunk:
                    break
                data += chunk
            except socket.timeout:
                break

        return data.decode('utf-8')

def test_service_access_granted():
    """Test that the service grants access for the correct base64 token."""
    host = '127.0.0.1'
    port = 9090
    payload = "c2VjcmV0X2FkbWluX3Rva2VuXzEyMw==\n"

    response = send_and_receive(host, port, payload)

    assert response == "ACCESS_GRANTED\n", (
        f"Expected 'ACCESS_GRANTED\\n' for correct token, but got: {repr(response)}"
    )

def test_service_access_denied():
    """Test that the service denies access for an incorrect base64 token."""
    host = '127.0.0.1'
    port = 9090
    payload = "aW52YWxpZF90b2tlbg==\n"  # base64 for "invalid_token"

    response = send_and_receive(host, port, payload)

    assert response == "ACCESS_DENIED\n", (
        f"Expected 'ACCESS_DENIED\\n' for incorrect token, but got: {repr(response)}"
    )