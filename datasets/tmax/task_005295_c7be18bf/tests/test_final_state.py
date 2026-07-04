# test_final_state.py

import os
import sqlite3
import socket
import requests
import pytest

def test_legacy_db_state():
    db_path = "/app/legacy.db"
    assert os.path.exists(db_path), f"Database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check table existence
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    assert cursor.fetchone() is not None, "Table 'users' does not exist in the database."

    # Check data
    cursor.execute("SELECT id, name, role FROM users WHERE id=1")
    row = cursor.fetchone()
    assert row is not None, "User with ID 1 does not exist."
    assert row[0] == 1, f"Expected user ID 1, got {row[0]}"
    assert row[1] == "mötley_user", f"Expected user name 'mötley_user', got {row[1]}"
    assert row[2] == "admin", f"Expected user role 'admin', got {row[2]}"
    conn.close()

def test_shared_library_exists():
    so_path = "/app/legacy_hash.so"
    assert os.path.exists(so_path), f"Shared library {so_path} was not compiled."

def test_http_service():
    url = "http://127.0.0.1:8080/user/1"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP request to {url} failed: {e}. Is the server running on port 8080?")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    expected_bytes = "1,mötley_user,admin".encode("windows-1252")
    assert response.content == expected_bytes, f"Expected response bytes {expected_bytes}, got {response.content}. Ensure windows-1252 encoding is used."

def test_tcp_service():
    host = "127.0.0.1"
    port = 8081

    try:
        with socket.create_connection((host, port), timeout=5) as s:
            s.sendall(b"TOKEN 1\n")
            data = s.recv(1024)
    except Exception as e:
        pytest.fail(f"TCP connection or communication to {host}:{port} failed: {e}. Is the TCP server running?")

    expected = b"999375\n"
    assert expected in data or data.strip() == b"999375", f"Expected TCP response {expected}, got {data}"