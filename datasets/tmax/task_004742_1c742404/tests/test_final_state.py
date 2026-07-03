# test_final_state.py

import os
import re
import socket
import pytest

def send_tcp_request(host, port, message):
    """Helper to send a message to the TCP server and read the response."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5.0)
            s.connect((host, port))
            s.sendall(message.encode('utf-8'))

            # Read response until newline or connection closed
            response = b""
            while True:
                chunk = s.recv(1024)
                if not chunk:
                    break
                response += chunk
                if b'\n' in response:
                    break
            return response.decode('utf-8')
    except Exception as e:
        pytest.fail(f"Failed to communicate with TCP server at {host}:{port}: {e}")

def test_tcp_server_valid_data_1():
    """Test the TCP server with valid data."""
    response = send_tcp_request('127.0.0.1', 7777, "TEST1,2.0,3.0,4.0\n")
    assert response == "SCORE: 29.00\n", f"Expected 'SCORE: 29.00\\n', got {repr(response)}"

def test_tcp_server_valid_data_2():
    """Test the TCP server with valid negative data."""
    response = send_tcp_request('127.0.0.1', 7777, "B99,-10.0,0.0,5.0\n")
    assert response == "SCORE: 125.00\n", f"Expected 'SCORE: 125.00\\n', got {repr(response)}"

def test_tcp_server_invalid_data_out_of_bounds():
    """Test the TCP server with out-of-bounds data."""
    response = send_tcp_request('127.0.0.1', 7777, "ERR1,150.0,10.0,10.0\n")
    assert response == "ERR: INVALID_DATA\n", f"Expected 'ERR: INVALID_DATA\\n', got {repr(response)}"

def test_tcp_server_invalid_data_format():
    """Test the TCP server with badly formatted data."""
    response = send_tcp_request('127.0.0.1', 7777, "BAD,1.0\n")
    assert response == "ERR: INVALID_DATA\n", f"Expected 'ERR: INVALID_DATA\\n', got {repr(response)}"

def test_cron_file_exists_and_content():
    """Test that the cron file exists and contains the correct expression."""
    cron_path = "/home/user/pipeline_cron"
    assert os.path.isfile(cron_path), f"Cron file {cron_path} does not exist."

    with open(cron_path, 'r') as f:
        content = f.read()

    lines = content.strip().split('\n')
    pattern = re.compile(r'^\s*\*/5\s+\*\s+\*\s+\*\s+\*\s+/home/user/batch_poll\.sh\s*$')

    match_found = any(pattern.match(line) for line in lines)
    assert match_found, f"Could not find the expected cron expression in {cron_path}. Content:\n{content}"