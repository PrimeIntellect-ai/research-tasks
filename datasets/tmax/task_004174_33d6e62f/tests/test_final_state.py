# test_final_state.py

import socket
import os
import pytest

def send_query(query: str) -> str:
    """Helper to send a query to the TCP server and return the response."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    try:
        s.connect(("127.0.0.1", 8080))
        s.sendall(query.encode("ascii"))
        response = s.recv(1024).decode("ascii")
    except Exception as e:
        pytest.fail(f"Failed to communicate with the server on 127.0.0.1:8080. Error: {e}")
    finally:
        s.close()
    return response

def test_c_source_exists():
    """Check that the student created the C program."""
    path = "/home/user/backup_verifier.c"
    assert os.path.isfile(path), f"File {path} does not exist."

def test_degree_queries():
    """Test the DEGREE command for various nodes."""
    # Graph is a line: 0-1-2-3-4-5
    # Node 0 has degree 1
    resp = send_query("DEGREE 0\n")
    assert resp.strip() == "1", f"Expected DEGREE 0 to be 1, got {resp!r}"

    # Node 1 has degree 2
    resp = send_query("DEGREE 1\n")
    assert resp.strip() == "2", f"Expected DEGREE 1 to be 2, got {resp!r}"

    # Node 5 has degree 1
    resp = send_query("DEGREE 5\n")
    assert resp.strip() == "1", f"Expected DEGREE 5 to be 1, got {resp!r}"

def test_path_queries():
    """Test the PATH command for various node pairs."""
    # Path from 0 to 5 is 5 edges
    resp = send_query("PATH 0 5\n")
    assert resp.strip() == "5", f"Expected PATH 0 5 to be 5, got {resp!r}"

    # Path from 2 to 4 is 2 edges
    resp = send_query("PATH 2 4\n")
    assert resp.strip() == "2", f"Expected PATH 2 4 to be 2, got {resp!r}"

    # Path from 3 to 3 is 0 edges
    resp = send_query("PATH 3 3\n")
    assert resp.strip() == "0", f"Expected PATH 3 3 to be 0, got {resp!r}"

    # Path from 5 to 0 is 5 edges
    resp = send_query("PATH 5 0\n")
    assert resp.strip() == "5", f"Expected PATH 5 0 to be 5, got {resp!r}"