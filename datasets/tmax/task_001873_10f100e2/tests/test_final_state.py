# test_final_state.py

import os
import socket
import time
import pytest

HOST = "127.0.0.1"
PORT = 8080

def send_query(s: socket.socket, query: str) -> str:
    s.sendall(query.encode("utf-8"))
    response = b""
    while b"\n" not in response:
        chunk = s.recv(4096)
        if not chunk:
            break
        response += chunk
    return response.decode("utf-8")

def test_tcp_server_responses():
    """Connect to the server and verify the responses for specific queries."""
    # Attempt to connect with retries in case the server is slow to start
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)

    connected = False
    for _ in range(5):
        try:
            s.connect((HOST, PORT))
            connected = True
            break
        except ConnectionRefusedError:
            time.sleep(1)

    assert connected, f"Failed to connect to TCP server at {HOST}:{PORT}"

    try:
        # Test A: descendants are B, C, D
        resp_a = send_query(s, "GET_DESCENDANTS A\n")
        assert resp_a == "B,C,D\n", f"Expected 'B,C,D\\n' for A, got {repr(resp_a)}"

        # Test B: descendants are D
        resp_b = send_query(s, "GET_DESCENDANTS B\n")
        assert resp_b == "D\n", f"Expected 'D\\n' for B, got {repr(resp_b)}"

        # Test C: no descendants
        resp_c = send_query(s, "GET_DESCENDANTS C\n")
        assert resp_c == "NONE\n", f"Expected 'NONE\\n' for C, got {repr(resp_c)}"

        # Test X: non-existent node
        resp_x = send_query(s, "GET_DESCENDANTS X\n")
        assert resp_x == "NONE\n", f"Expected 'NONE\\n' for X, got {repr(resp_x)}"
    finally:
        s.close()

def test_source_code_exists():
    """Verify that the user wrote the server code in the expected location."""
    source_path = "/home/user/graph_server.c"
    assert os.path.isfile(source_path), f"Source file missing: {source_path}"

def test_query_log_exists_and_contains_queries():
    """Verify that the query log exists and contains the queries we just sent."""
    log_path = "/home/user/query_log.txt"
    assert os.path.isfile(log_path), f"Query log missing: {log_path}"

    with open(log_path, "r") as f:
        content = f.read()

    assert "GET_DESCENDANTS A" in content, "Query log does not contain 'GET_DESCENDANTS A'"
    assert "GET_DESCENDANTS B" in content, "Query log does not contain 'GET_DESCENDANTS B'"
    assert "GET_DESCENDANTS C" in content, "Query log does not contain 'GET_DESCENDANTS C'"
    assert "GET_DESCENDANTS X" in content, "Query log does not contain 'GET_DESCENDANTS X'"