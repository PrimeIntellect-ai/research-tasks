# test_final_state.py
import os
import sqlite3
import pytest
import requests

DB_PATH = "/app/db/timeseries.sqlite3"
API_URL = "http://127.0.0.1:8000/data"
VALID_HEADERS = {"Authorization": "Bearer ops_token_99"}
INVALID_HEADERS = {"Authorization": "Bearer wrong_token"}

def test_sqlite_db_exists_and_data_correct():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} does not exist."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='hourly_data';")
    assert cursor.fetchone() is not None, "Table 'hourly_data' does not exist in the database."

    # Check row count
    cursor.execute("SELECT COUNT(*) FROM hourly_data;")
    count = cursor.fetchone()[0]
    assert count == 3, f"Expected 3 rows in hourly_data, found {count}."

    # Check specific aggregated data
    cursor.execute("SELECT sensor_id, hour_ts, avg_val FROM hourly_data ORDER BY sensor_id, hour_ts;")
    rows = cursor.fetchall()

    expected_rows = [
        ("sensor_A", "2024-10-01T10:00:00", 38.5),
        ("sensor_A", "2024-10-01T11:00:00", 35.0),
        ("sensor_B", "2024-10-01T10:00:00", 77.0)
    ]

    for row in expected_rows:
        assert row in rows, f"Expected row {row} not found in database. Actual rows: {rows}"

    conn.close()

def test_api_unauthorized():
    try:
        response = requests.get(f"{API_URL}?sensor_id=sensor_A", headers=INVALID_HEADERS, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for invalid token, got {response.status_code}."

def test_api_sensor_a():
    try:
        response = requests.get(f"{API_URL}?sensor_id=sensor_A", headers=VALID_HEADERS, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for sensor_A, got {response.status_code}."
    data = response.json()

    expected_data = [
        {"hour_ts": "2024-10-01T10:00:00", "avg_val": 38.5},
        {"hour_ts": "2024-10-01T11:00:00", "avg_val": 35.0}
    ]

    assert data == expected_data, f"API response for sensor_A did not match expected. Got: {data}"

def test_api_sensor_b():
    try:
        response = requests.get(f"{API_URL}?sensor_id=sensor_B", headers=VALID_HEADERS, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for sensor_B, got {response.status_code}."
    data = response.json()

    expected_data = [
        {"hour_ts": "2024-10-01T10:00:00", "avg_val": 77.0}
    ]

    assert data == expected_data, f"API response for sensor_B did not match expected. Got: {data}"