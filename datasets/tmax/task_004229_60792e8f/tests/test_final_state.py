# test_final_state.py
import os
import socket
import sqlite3
import pytest

def test_database_indexes():
    """Verify that indexes were created on paper_authors."""
    db_path = "/app/dataset.db"
    assert os.path.isfile(db_path), f"Database file missing: {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index' AND tbl_name='paper_authors'")
    indexes = cursor.fetchall()
    conn.close()

    assert len(indexes) > 0, "No indexes found on the 'paper_authors' table. The agent must create optimal indexes."

def test_tcp_server_responses():
    """Verify the TCP server is running and responds correctly to requests."""
    host = "127.0.0.1"
    port = 9000

    queries_and_expected = [
        ("GET_COAUTHORS 2\n", "1,3,4\n"),
        ("GET_COAUTHORS 1\n", "2,3\n"),
        ("GET_COAUTHORS 5\n", "\n"),
        ("GET_COAUTHORS 99\n", "\n")
    ]

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5.0)
        s.connect((host, port))
    except Exception as e:
        pytest.fail(f"Failed to connect to TCP server at {host}:{port}: {e}")

    try:
        for req, expected in queries_and_expected:
            s.sendall(req.encode('utf-8'))

            # Read until newline
            resp = b""
            while True:
                chunk = s.recv(1024)
                if not chunk:
                    break
                resp += chunk
                if b"\n" in chunk:
                    break

            resp_str = resp.decode('utf-8')
            assert resp_str == expected, f"Expected '{expected.strip()}' for request '{req.strip()}', but got '{resp_str.strip()}'"
    finally:
        s.close()