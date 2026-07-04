# test_final_state.py

import socket
import pytest
import time

HOST = '127.0.0.1'
PORT = 9090

def send_command(command: str, expect_response: bool = True) -> str:
    """Helper to send a command to the TCP server and get the response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2.0)
        try:
            s.connect((HOST, PORT))
        except ConnectionRefusedError:
            pytest.fail(f"Could not connect to {HOST}:{PORT}. Is the server running?")

        s.sendall(command.encode('utf-8'))

        if not expect_response:
            try:
                response = s.recv(1024)
                if response:
                    return response.decode('utf-8')
            except (socket.timeout, ConnectionResetError):
                return ""
            return ""

        try:
            response = s.recv(1024)
            return response.decode('utf-8')
        except socket.timeout:
            pytest.fail(f"Timeout waiting for response to command: {command.strip()}")
        except ConnectionResetError:
            pytest.fail(f"Connection reset by peer when sending command: {command.strip()}")

def test_get_mean():
    response = send_command("GET_MEAN\n")
    assert response.strip() == "Mean: 20.50", f"Expected 'Mean: 20.50', got '{response.strip()}'"

def test_get_ci():
    response = send_command("GET_CI\n")
    assert response.strip() == "CI: [20.16, 20.84]", f"Expected 'CI: [20.16, 20.84]', got '{response.strip()}'"

def test_get_outlier_count_auth():
    response = send_command("AUTH mysecrettoken GET_OUTLIER_COUNT\n")
    assert response.strip() == "Outliers: 1", f"Expected 'Outliers: 1', got '{response.strip()}'"

def test_get_outlier_count_no_auth():
    response = send_command("GET_OUTLIER_COUNT\n", expect_response=False)
    # The connection should be dropped, so response should be empty
    assert response.strip() == "", f"Expected connection drop or no response, but got '{response.strip()}'"