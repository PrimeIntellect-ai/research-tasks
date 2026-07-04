# test_final_state.py

import socket
import pytest

def send_request(host, port, payload):
    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            sock.sendall(payload.encode('utf-8'))
            response = sock.recv(1024).decode('utf-8')
            return response
    except ConnectionRefusedError:
        pytest.fail(f"Connection refused to {host}:{port}. Is the server running?")
    except socket.timeout:
        pytest.fail(f"Connection to {host}:{port} timed out.")
    except Exception as e:
        pytest.fail(f"Unexpected error communicating with server: {e}")

@pytest.mark.parametrize("query, expected", [
    ("café\n", "12.50\n"),
    ("DROP\n", "NOT_FOUND\n"),
    ("apple\n", "5.00\n"),
    ("unknown_token\n", "NOT_FOUND\n")
])
def test_tcp_server_responses(query, expected):
    """Test the TCP server responses for given queries."""
    host = "127.0.0.1"
    port = 9090

    response = send_request(host, port, query)
    assert response == expected, f"Expected '{expected}' for query '{query}', but got '{response}'"