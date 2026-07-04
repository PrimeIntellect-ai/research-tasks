# test_final_state.py

import os
import socket
import pytest

def send_request(host, port, message):
    """Helper function to send a message to the TCP server and receive the response."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5.0)
            s.connect((host, port))
            s.sendall(message.encode('utf-8'))
            response = s.recv(1024).decode('utf-8')
            return response
    except Exception as e:
        pytest.fail(f"Failed to connect to or receive data from the server at {host}:{port}. Error: {e}")

@pytest.mark.parametrize("bucket, expected_response", [
    ("0\n", "welcome to the system [LOC-EN]\n"),
    ("10\n", "please enter your password [LOC-EN]\n"),
    ("20\n", "login successful [LOC-EN]\n"),
    ("30\n", "EMPTY [LOC-EN]\n")
])
def test_tcp_server_responses(bucket, expected_response):
    """Test that the TCP server returns the correct bucketed and cleaned text."""
    host = "127.0.0.1"
    port = 9090

    response = send_request(host, port, bucket)
    assert response == expected_response, f"Expected '{expected_response}' for bucket '{bucket.strip()}', but got '{response}'"

def test_c_source_code_exists():
    """Test that the C source code file exists at the expected location."""
    c_file_path = "/home/user/loc_server.c"
    assert os.path.isfile(c_file_path), f"The C source code file is missing: {c_file_path}"