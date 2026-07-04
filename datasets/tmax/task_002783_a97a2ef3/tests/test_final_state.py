# test_final_state.py

import os
import socket
import sqlite3
import pytest

def transform(x: int) -> int:
    x = x & 0xFFFFFFFF
    val = (x * 1664525) + 1013904223
    val = val & 0xFFFFFFFF
    return val ^ (x >> 16)

def send_tcp_request(host: str, port: int, message: str) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2.0)
        s.connect((host, port))
        s.sendall(message.encode('utf-8'))
        response = b""
        while True:
            chunk = s.recv(1024)
            if not chunk:
                break
            response += chunk
            if b'\n' in response:
                break
        return response.decode('utf-8')

def test_service_valid_requests():
    host = "127.0.0.1"
    port = 9090

    test_cases = [10, 9999, 123456, 0, 4294967295]

    for val in test_cases:
        expected_output = transform(val)
        message = f"GENERATE {val} AUTH ci_cd_pipe_88\n"
        try:
            response = send_tcp_request(host, port, message)
        except Exception as e:
            pytest.fail(f"Failed to connect or receive from service for valid request: {e}")

        assert response == f"SUCCESS {expected_output}\n", f"Service returned incorrect response for input {val}: {response!r}"

def test_service_invalid_requests():
    host = "127.0.0.1"
    port = 9090

    invalid_messages = [
        "GENERATE 10 AUTH wrong_secret\n",
        "GENERATE 10 AUTH\n",
        "GENERATE AUTH ci_cd_pipe_88\n",
        "INVALID FORMAT\n",
        "GENERATE 10 AUTH ci_cd_pipe_88 extra\n"
    ]

    for msg in invalid_messages:
        try:
            response = send_tcp_request(host, port, msg)
        except Exception as e:
            pytest.fail(f"Failed to connect or receive from service for invalid request: {e}")

        assert response == "ERROR\n", f"Service did not return ERROR\\n for invalid request {msg!r}. Got: {response!r}"

def test_metrics_v2_db_migration():
    db_path = "/home/user/metrics_v2.db"
    assert os.path.exists(db_path), f"Missing migrated database at {db_path}"
    assert os.path.isfile(db_path), f"{db_path} is not a file"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if auth_logs table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auth_logs';")
    assert cursor.fetchone() is not None, "Table 'auth_logs' does not exist in migrated database"

    # Check schema
    cursor.execute("PRAGMA table_info(auth_logs);")
    columns = {row[1]: row[2] for row in cursor.fetchall()}
    assert "log_id" in columns, "Column 'log_id' missing from auth_logs table"
    assert "requested_val" in columns, "Column 'requested_val' missing from auth_logs table"
    assert "generated_val" in columns, "Column 'generated_val' missing from auth_logs table"
    assert "migration_date" in columns, "Column 'migration_date' missing from auth_logs table"

    # Check data
    cursor.execute("SELECT requested_val, generated_val, migration_date FROM auth_logs ORDER BY requested_val;")
    rows = cursor.fetchall()

    expected_inputs = [10, 9999, 123456]
    expected_data = sorted([
        (val, transform(val), "2023-10-01") for val in expected_inputs
    ], key=lambda x: x[0])

    assert len(rows) == len(expected_data), f"Expected {len(expected_data)} rows in auth_logs table, found {len(rows)}"

    for i, (expected, actual) in enumerate(zip(expected_data, rows)):
        assert expected == actual, f"Row mismatch: expected {expected}, got {actual}"

    conn.close()