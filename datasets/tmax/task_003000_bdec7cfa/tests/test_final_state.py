# test_final_state.py

import os
import socket
import sqlite3
import pytest

def test_index_dropped():
    db_path = "/home/user/pipeline.db"
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check that idx_stale has been dropped
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_stale';")
    result = cursor.fetchone()

    conn.close()

    assert result is None, "The corrupted index 'idx_stale' was not dropped from the database."

def _query_server(node_id: str) -> str:
    host = "127.0.0.1"
    port = 8888

    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            sock.sendall(f"{node_id}\n".encode('utf-8'))
            response = sock.recv(1024).decode('utf-8')
            return response
    except Exception as e:
        pytest.fail(f"Failed to connect to or read from TCP server at {host}:{port}: {e}")

def test_tcp_server_alpha():
    response = _query_server("Alpha")
    assert response == "IN:1,OUT:2\n", f"Expected 'IN:1,OUT:2\\n' for Node 'Alpha', got {repr(response)}"

def test_tcp_server_delta():
    response = _query_server("Delta")
    assert response == "IN:2,OUT:0\n", f"Expected 'IN:2,OUT:0\\n' for Node 'Delta', got {repr(response)}"

def test_tcp_server_beta():
    response = _query_server("Beta")
    assert response == "IN:1,OUT:1\n", f"Expected 'IN:1,OUT:1\\n' for Node 'Beta', got {repr(response)}"

def test_tcp_server_unknown():
    response = _query_server("Unknown")
    assert response == "IN:0,OUT:0\n", f"Expected 'IN:0,OUT:0\\n' for Node 'Unknown', got {repr(response)}"