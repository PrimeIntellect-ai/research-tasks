# test_final_state.py

import socket
import pytest

HOST = '127.0.0.1'
PORT = 8888

def send_request(ts_str: str) -> str:
    """Helper to send a request to the TCP server and read the response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5.0)
        s.connect((HOST, PORT))
        s.sendall(f"{ts_str}\n".encode('utf-8'))

        response = b""
        while True:
            chunk = s.recv(1024)
            if not chunk:
                break
            response += chunk
            if b'\n' in chunk:
                break

        return response.decode('utf-8')

@pytest.mark.parametrize("timestamp, expected", [
    ("1680000000", "11.50\n"),
    ("1680000004", "15.50\n"),
    ("1680000005", "15.50\n"),
    ("1680000006", "99.90\n"),
    ("1680000007", "99.90\n"),
    ("1680000015", "0.50\n"),
    ("1679999999", "NOT_FOUND\n")
])
def test_tcp_server_responses(timestamp, expected):
    """
    Verify that the TCP server responds with the correct processed value 
    for the given timestamp.
    """
    try:
        response = send_request(timestamp)
    except ConnectionRefusedError:
        pytest.fail(f"Connection refused to {HOST}:{PORT}. The server is not running or listening on the correct port.")
    except socket.timeout:
        pytest.fail(f"Connection to {HOST}:{PORT} timed out. The server might be hanging.")
    except Exception as e:
        pytest.fail(f"Unexpected error when communicating with server: {e}")

    assert response == expected, f"For timestamp {timestamp}, expected {repr(expected)} but got {repr(response)}"