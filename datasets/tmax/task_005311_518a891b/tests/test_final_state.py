# test_final_state.py

import os
import pytest
import requests
import socket
import sqlite3
import json

HTTP_URL = "http://127.0.0.1:8080/encode"
TCP_HOST = "127.0.0.1"
TCP_PORT = 9090
DB_PATH = "/home/user/service/data.db"

def test_http_endpoint():
    """Verify the HTTP endpoint works and handles long sequences without crashing."""
    try:
        resp1 = requests.post(HTTP_URL, json={"text": "AABBBCCCC"}, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP server: {e}")

    assert resp1.status_code == 200, f"Expected HTTP 200, got {resp1.status_code}"
    try:
        data1 = resp1.json()
    except json.JSONDecodeError:
        pytest.fail(f"Expected JSON response, got: {resp1.text}")

    assert "encoded" in data1, "Response JSON missing 'encoded' key"
    assert data1["encoded"] in ["2A3B4C", "A2B3C4", "A2B3C4", "2A3B4C"], f"Unexpected encoding format: {data1['encoded']}"

    # Test long sequence to trigger UB if not fixed
    try:
        resp2 = requests.post(HTTP_URL, json={"text": "AAAAAAAAAAAAAAAA"}, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP server for long sequence: {e}")

    assert resp2.status_code == 200, f"Expected HTTP 200, got {resp2.status_code}"
    data2 = resp2.json()
    assert "encoded" in data2, "Response JSON missing 'encoded' key"
    assert data2["encoded"] in ["16A", "A16"], f"Unexpected encoding format for long sequence: {data2['encoded']}"

def test_tcp_endpoint():
    """Verify the TCP endpoint works and returns the encoded string."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect((TCP_HOST, TCP_PORT))
        s.sendall(b"WWWWWWWWWWWW\n")
        data = s.recv(1024).decode("utf-8")
        assert data in ["12W\n", "W12\n"], f"Unexpected TCP response: {repr(data)}"
    except socket.error as e:
        pytest.fail(f"TCP connection or communication failed: {e}")
    finally:
        s.close()

def test_sqlite_database():
    """Verify the SQLite database contains the processed records."""
    assert os.path.exists(DB_PATH), f"Database not found at {DB_PATH}"

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT original, encoded FROM processed_data;")
        rows = cursor.fetchall()
    except sqlite3.Error as e:
        pytest.fail(f"Database query failed: {e}")
    finally:
        conn.close()

    originals = [row[0] for row in rows]
    assert "AABBBCCCC" in originals, "Missing 'AABBBCCCC' in database"
    assert "AAAAAAAAAAAAAAAA" in originals, "Missing 'AAAAAAAAAAAAAAAA' in database"
    assert "WWWWWWWWWWWW" in originals, "Missing 'WWWWWWWWWWWW' in database"

def test_rle_c_library_built():
    """Verify the vendored C library was successfully built."""
    lib_path = "/app/rle-c-1.0.0/librle.a"
    assert os.path.exists(lib_path), f"Static library {lib_path} was not built."