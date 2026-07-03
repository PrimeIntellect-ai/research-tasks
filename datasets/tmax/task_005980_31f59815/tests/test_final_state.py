# test_final_state.py

import os
import sqlite3
import urllib.request
import json
import time
import pytest

def test_libmath_so_exists():
    assert os.path.isfile("/home/user/libmath.so"), "The shared library /home/user/libmath.so does not exist."

def test_server_pid_and_running():
    pid_file = "/home/user/server.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} does not exist."
    with open(pid_file, "r") as f:
        pid_str = f.read().strip()
    assert pid_str.isdigit(), "PID file does not contain a valid integer."
    pid = int(pid_str)

    # Check if process is running
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} is not running.")

def test_database_schema_migration():
    db_path = "/home/user/metrics.db"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(calculations);")
    columns = cursor.fetchall()

    timestamp_col = next((col for col in columns if col[1] == 'timestamp'), None)
    assert timestamp_col is not None, "Column 'timestamp' was not added to 'calculations' table."

    # col[2] is type, col[4] is default value
    assert timestamp_col[2].upper() == 'DATETIME', "Column 'timestamp' is not of type DATETIME."
    assert timestamp_col[4] is not None and 'CURRENT_TIMESTAMP' in timestamp_col[4].upper(), "Column 'timestamp' does not have DEFAULT CURRENT_TIMESTAMP."

    conn.close()

def test_server_endpoint_and_db_logging():
    # Make a request to the server
    url_5 = "http://localhost:8080/prime/5"
    try:
        req = urllib.request.Request(url_5)
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
    except Exception as e:
        pytest.fail(f"Failed to make request to {url_5}: {e}")

    assert data.get("n") == 5, f"Expected n=5 in response, got {data.get('n')}"
    assert data.get("result") == 11, f"Expected result=11 for 5th prime, got {data.get('result')}"

    url_10 = "http://localhost:8080/prime/10"
    try:
        req = urllib.request.Request(url_10)
        with urllib.request.urlopen(req, timeout=5) as response:
            data_10 = json.loads(response.read().decode())
    except Exception as e:
        pytest.fail(f"Failed to make request to {url_10}: {e}")

    assert data_10.get("n") == 10, f"Expected n=10 in response, got {data_10.get('n')}"
    assert data_10.get("result") == 29, f"Expected result=29 for 10th prime, got {data_10.get('result')}"

    # Verify database logging
    db_path = "/home/user/metrics.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM calculations WHERE n=5 AND result=11;")
    count_5 = cursor.fetchone()[0]
    assert count_5 >= 1, "The request for n=5, result=11 was not logged in the database."

    cursor.execute("SELECT COUNT(*) FROM calculations WHERE n=10 AND result=29;")
    count_10 = cursor.fetchone()[0]
    assert count_10 >= 1, "The request for n=10, result=29 was not logged in the database."

    conn.close()