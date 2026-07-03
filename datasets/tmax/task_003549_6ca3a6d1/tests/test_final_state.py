# test_final_state.py

import os
import sqlite3
import pytest
import requests
import re

APP_DIR = "/home/user/app"
BACKEND_DIR = os.path.join(APP_DIR, "backend")
DATA_DIR = os.path.join(APP_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "analytics.db")

def test_libanalyzer_built():
    libanalyzer_so = os.path.join(BACKEND_DIR, "libanalyzer.so")
    assert os.path.isfile(libanalyzer_so), f"Missing shared library: {libanalyzer_so}. Did you compile analyzer.c?"

def test_database_schema_and_data_migrated():
    assert os.path.isfile(DB_PATH), f"Missing database file: {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(events);")
    columns = cursor.fetchall()

    timestamp_col = next((col for col in columns if col[1] == 'timestamp'), None)
    assert timestamp_col is not None, "Column 'timestamp' does not exist in 'events' table"
    assert timestamp_col[2].upper() == 'TEXT', f"Column 'timestamp' should be of type TEXT, found {timestamp_col[2]}"

    iso_time_col = next((col for col in columns if col[1] == 'iso_time'), None)
    assert iso_time_col is None, "Column 'iso_time' should have been renamed to 'timestamp'"

    cursor.execute("SELECT timestamp FROM events LIMIT 10;")
    rows = cursor.fetchall()
    assert len(rows) > 0, "No data found in events table"

    iso8601_regex = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$')
    for row in rows:
        ts = row[0]
        assert isinstance(ts, str), f"Timestamp '{ts}' is not a string"
        assert iso8601_regex.match(ts), f"Timestamp '{ts}' is not in the expected ISO 8601 format (e.g., 2023-10-05T14:48:00Z)"

    conn.close()

def test_api_valid_request():
    url = "http://127.0.0.1:8080/ingest"
    payload = {
        "user_id": 42,
        "event_type": "login",
        "metadata": {
            "ip": "192.168.1.1",
            "attempts": 3
        }
    }
    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert data.get("status") == "success", f"Expected status 'success', got {data.get('status')}"

    expected_score = 3 * 1.5 + 42 % 10  # 6.5
    assert data.get("risk_score") == expected_score, f"Expected risk_score {expected_score}, got {data.get('risk_score')}"

def test_api_invalid_request_validation():
    url = "http://127.0.0.1:8080/ingest"
    # Invalid because attempts > 5
    payload = {
        "user_id": 42,
        "event_type": "login",
        "metadata": {
            "ip": "192.168.1.1",
            "attempts": 6
        }
    }
    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert response.status_code == 400, f"Expected HTTP 400 for validation failure, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert data.get("error") == "Validation failed", f"Expected error 'Validation failed', got {data.get('error')}"

def test_api_missing_fields_validation():
    url = "http://127.0.0.1:8080/ingest"
    # Missing metadata
    payload = {
        "user_id": 42,
        "event_type": "login"
    }
    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert response.status_code == 400, f"Expected HTTP 400 for missing fields validation failure, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert data.get("error") == "Validation failed", f"Expected error 'Validation failed', got {data.get('error')}"