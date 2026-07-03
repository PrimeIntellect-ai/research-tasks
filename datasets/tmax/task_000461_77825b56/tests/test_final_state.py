# test_final_state.py

import socket
import time
import pytest

def test_recommendation_service():
    """Connect to the recommendation service on 127.0.0.1:8888 and verify its response."""
    host = '127.0.0.1'
    port = 8888

    # Try to connect, with retries in case the service is slow to start
    max_retries = 5
    connected = False
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)

    for _ in range(max_retries):
        try:
            s.connect((host, port))
            connected = True
            break
        except (ConnectionRefusedError, socket.timeout):
            time.sleep(1)

    assert connected, f"Could not connect to service at {host}:{port}"

    try:
        # Send request
        s.sendall(b"101\n")

        # Receive response
        response = s.recv(1024).decode('utf-8').strip()

        # Verify response
        expected_response = "102,104,103"
        assert response == expected_response, f"Expected response '{expected_response}', but got '{response}'"

    finally:
        s.close()

def test_recommendation_service_multiple_requests():
    """Verify that the service can handle multiple sequential requests."""
    host = '127.0.0.1'
    port = 8888

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)

    try:
        s.connect((host, port))
    except (ConnectionRefusedError, socket.timeout):
        pytest.fail(f"Could not connect to service at {host}:{port} for second test")

    try:
        # First request
        s.sendall(b"101\n")
        response1 = s.recv(1024).decode('utf-8').strip()
        assert response1 == "102,104,103", f"First request failed: got '{response1}'"

        # Second request (same connection if keep-alive, or we might need to reconnect depending on nc usage)
        # The prompt says: "The server should remain open to handle multiple sequential requests"
        # Usually this means the same connection if using nc -k, or a new connection.
        # Let's try on the same connection first.
        s.sendall(b"101\n")
        response2 = s.recv(1024).decode('utf-8').strip()

        # If response2 is empty, it might have closed the connection. Let's reconnect.
        if not response2:
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2.0)
            s.connect((host, port))
            s.sendall(b"101\n")
            response2 = s.recv(1024).decode('utf-8').strip()

        assert response2 == "102,104,103", f"Second request failed: got '{response2}'"

    finally:
        s.close()