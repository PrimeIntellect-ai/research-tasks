# test_final_state.py
import os
import socket
import time

def test_server_script_exists():
    script_path = "/home/user/server.sh"
    assert os.path.isfile(script_path), f"The script {script_path} is missing."

def test_tcp_server_processing():
    payload = """line 1
line 2
line 3
CORRUPT line
line 4
line 5
line 6
line 7
line 8
line 9
line 10
line 11
line 12
line 13
line 14
CORRUPT data
line 15
line 16
line 17
line 18
line 19
line 20
line 21
line 22
line 23
"""

    expected_output = """PROCESSED: line 1
PROCESSED: line 2
PROCESSED: line 3
PROCESSED: line 4
PROCESSED: line 5
PROCESSED: line 6
PROCESSED: line 7
PROCESSED: line 8
PROCESSED: line 9
PROCESSED: line 10
PROCESSED: line 11
PROCESSED: line 12
PROCESSED: line 13
PROCESSED: line 14
PROCESSED: line 15
PROCESSED: line 16
PROCESSED: line 17
PROCESSED: line 18
PROCESSED: line 19
PROCESSED: line 20
PROCESSED: line 21
PROCESSED: line 22
PROCESSED: line 23
"""

    host = '127.0.0.1'
    port = 8000

    # Try connecting with retries in case the server is slow to start
    max_retries = 5
    sock = None
    for i in range(max_retries):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5.0)
            sock.connect((host, port))
            break
        except ConnectionRefusedError:
            if i == max_retries - 1:
                assert False, f"Could not connect to {host}:{port}. Is the server running?"
            time.sleep(1)

    try:
        # Send payload
        sock.sendall(payload.encode('utf-8'))
        # Half-close the socket to signal EOF to the server
        sock.shutdown(socket.SHUT_WR)

        # Read response
        response = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk

        response_str = response.decode('utf-8')

        assert response_str == expected_output, (
            f"Server response did not match expected output.\n"
            f"Expected:\n{expected_output}\n"
            f"Got:\n{response_str}"
        )

    finally:
        sock.close()