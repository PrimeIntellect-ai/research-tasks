# test_final_state.py

import os
import socket
import pytest

HOST = "127.0.0.1"
PORT = 8080

def test_server_cov_response():
    """Test that the server responds correctly to the COV command."""
    expected_cov_file = "/truth_cov.txt"
    assert os.path.exists(expected_cov_file), f"Truth file {expected_cov_file} missing."

    with open(expected_cov_file, "r") as f:
        expected_cov = f.read().strip()

    try:
        with socket.create_connection((HOST, PORT), timeout=5) as s:
            s.sendall(b"COV\n")
            response = s.recv(4096).decode("ascii").strip()
    except ConnectionRefusedError:
        pytest.fail(f"Could not connect to server at {HOST}:{PORT}")
    except socket.timeout:
        pytest.fail(f"Server at {HOST}:{PORT} timed out waiting for COV response.")

    assert response == expected_cov, f"Expected COV response '{expected_cov}', got '{response}'"

def test_server_trace_response():
    """Test that the server responds correctly to the TRACE command."""
    expected_trace_file = "/truth_trace.txt"
    assert os.path.exists(expected_trace_file), f"Truth file {expected_trace_file} missing."

    with open(expected_trace_file, "r") as f:
        expected_trace = f.read().strip()

    try:
        with socket.create_connection((HOST, PORT), timeout=5) as s:
            s.sendall(b"TRACE\n")
            response = s.recv(4096).decode("ascii").strip()
    except ConnectionRefusedError:
        pytest.fail(f"Could not connect to server at {HOST}:{PORT}")
    except socket.timeout:
        pytest.fail(f"Server at {HOST}:{PORT} timed out waiting for TRACE response.")

    assert response == expected_trace, f"Expected TRACE response '{expected_trace}', got '{response}'"