# test_final_state.py

import socket
import pytest

def test_tcp_server_response():
    """
    Connect to the TCP server on port 9099, send FETCH_STATS, 
    and verify the aggregated latency statistics response.
    """
    host = '127.0.0.1'
    port = 9099

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5.0)
            s.connect((host, port))
            s.sendall(b"FETCH_STATS\n")

            data = b""
            while True:
                try:
                    chunk = s.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                except socket.timeout:
                    break
    except ConnectionRefusedError:
        pytest.fail(f"Connection refused on {host}:{port}. Ensure the server is listening.")
    except socket.timeout:
        pytest.fail(f"Connection timed out on {host}:{port}.")
    except Exception as e:
        pytest.fail(f"Unexpected error connecting to {host}:{port}: {e}")

    response = data.decode('utf-8', errors='replace').strip()

    expected_lines = [
        "2023-10-15 08:00 -> 125",
        "2023-10-15 09:00 -> 210"
    ]

    response_lines = [line.strip() for line in response.split('\n') if line.strip()]

    assert response_lines == expected_lines, (
        f"Server response did not match expected output.\n"
        f"Expected: {expected_lines}\n"
        f"Got: {response_lines}"
    )