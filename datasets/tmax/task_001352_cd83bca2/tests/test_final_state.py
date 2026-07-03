# test_final_state.py

import os
import sqlite3
import subprocess
import socket
import requests
import pytest

def test_rust_compilation():
    binary_path = "/app/rust_counter/target/release/rust_counter"
    assert os.path.isfile(binary_path), f"Rust release binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Rust binary at {binary_path} is not executable"

    # Check if it runs without crashing
    try:
        result = subprocess.run([binary_path, "hello world"], capture_output=True, text=True, timeout=2)
        assert result.returncode == 0, f"Rust binary exited with non-zero code: {result.returncode}\nStderr: {result.stderr}"
    except subprocess.TimeoutExpired:
        pytest.fail("Rust binary timed out during execution.")

def test_schema_migration():
    db_path = "/app/video_stats.db"
    assert os.path.isfile(db_path), f"SQLite database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(stats)")
    columns = {row[1]: row[2] for row in cursor.fetchall()}
    assert "anomalies" in columns, "Column 'anomalies' missing in stats table."

    cursor.execute("SELECT anomalies FROM stats WHERE video_name = 'traffic.mp4'")
    row = cursor.fetchone()
    assert row is not None, "Row for 'traffic.mp4' missing in stats table."
    assert row[0] == 3, f"Expected anomalies to be 3 for traffic.mp4, got {row[0]}."

    conn.close()

def test_video_fixture():
    frame_path = "/app/frame_30.jpg"
    assert os.path.isfile(frame_path), f"Frame image {frame_path} does not exist."

    with open(frame_path, "rb") as f:
        header = f.read(2)
    assert header == b"\xff\xd8", f"File {frame_path} does not appear to be a valid JPEG."

def test_http_evaluate_endpoint():
    url = "http://127.0.0.1:8000/evaluate"

    test_cases = [
        ("10 + 2 * 6", 22),
        ("3 + 5 * 2", 13),
        ("10 - 2", 8),
        ("20 / 4 + 3", 8)
    ]

    for expr, expected in test_cases:
        try:
            response = requests.post(url, json={"expr": expr}, timeout=2)
        except requests.RequestException as e:
            pytest.fail(f"Failed to connect to HTTP evaluate endpoint: {e}")

        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"Response is not valid JSON: {response.text}")

        assert "result" in data, f"Key 'result' missing in JSON response: {data}"
        assert data["result"] == expected, f"Expected result {expected} for expression '{expr}', got {data['result']}"

def test_http_frame_endpoint():
    url = "http://127.0.0.1:8000/frame"
    frame_path = "/app/frame_30.jpg"

    try:
        response = requests.get(url, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP frame endpoint: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    with open(frame_path, "rb") as f:
        expected_bytes = f.read()

    assert response.content == expected_bytes, "Returned bytes do not match the contents of /app/frame_30.jpg"

def test_tcp_evaluate_endpoint():
    host = "127.0.0.1"
    port = 8001

    test_cases = [
        ("4 * 4 + 4\n", "20\n"),
        ("10 - 2\n", "8\n"),
        ("15 / 3 + 2\n", "7\n")
    ]

    for expr, expected in test_cases:
        try:
            with socket.create_connection((host, port), timeout=2) as s:
                s.sendall(expr.encode('utf-8'))
                data = s.recv(1024).decode('utf-8')
                assert data == expected, f"Expected TCP response '{expected}' for expression '{expr}', got '{data}'"
        except socket.error as e:
            pytest.fail(f"TCP connection or communication failed: {e}")