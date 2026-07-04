# test_final_state.py

import os
import sqlite3
import json
import uuid
import requests
import pytest

def encode_log(log_str: str) -> str:
    """Encode log string using the obfuscator logic: XOR with 0x5C, then hex encode."""
    return bytes([b ^ 0x5C for b in log_str.encode('utf-8')]).hex()

def test_ingest_endpoint_and_database():
    url = "http://127.0.0.1:8000/api/v1/ingest"

    # Prepare test data
    batch_id = str(uuid.uuid4())
    raw_logs = [
        "2023-10-01T12:00:00Z|192.168.001.001|warn|User login failed",
        "2023-10-01T12:00:01Z|010.000.000.002|error|Database connection lost",
        "2023-10-01T12:00:02Z|172.016.254.001|info|Service started successfully"
    ]

    expected_normalized = [
        ("2023-10-01T12:00:00Z", "192.168.1.1", "WARN", "User login failed"),
        ("2023-10-01T12:00:01Z", "10.0.0.2", "ERROR", "Database connection lost"),
        ("2023-10-01T12:00:02Z", "172.16.254.1", "INFO", "Service started successfully")
    ]

    obfuscated_logs = [encode_log(log) for log in raw_logs]

    payload = {
        "batch_id": batch_id,
        "obfuscated_logs": obfuscated_logs
    }

    # Send request
    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the ingestion service at {url}. Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        resp_json = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert resp_json.get("status") == "success", f"Expected status 'success', got {resp_json.get('status')}"
    assert resp_json.get("processed_count") == len(raw_logs), f"Expected processed_count {len(raw_logs)}, got {resp_json.get('processed_count')}"

    # Check database
    db_path = "/home/user/logs.db"
    assert os.path.exists(db_path), f"Database file not found at {db_path}"

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT timestamp, ip, severity, message FROM system_logs WHERE batch_id = ? ORDER BY timestamp ASC", (batch_id,))
        rows = cursor.fetchall()

        assert len(rows) == len(expected_normalized), f"Expected {len(expected_normalized)} rows in DB for batch {batch_id}, found {len(rows)}"

        for i, row in enumerate(rows):
            expected = expected_normalized[i]
            assert row[0] == expected[0], f"Timestamp mismatch: expected {expected[0]}, got {row[0]}"
            assert row[1] == expected[1], f"IP mismatch: expected {expected[1]}, got {row[1]}"
            assert row[2] == expected[2], f"Severity mismatch: expected {expected[2]}, got {row[2]}"
            assert row[3] == expected[3], f"Message mismatch: expected {expected[3]}, got {row[3]}"

    except sqlite3.Error as e:
        pytest.fail(f"Database error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()