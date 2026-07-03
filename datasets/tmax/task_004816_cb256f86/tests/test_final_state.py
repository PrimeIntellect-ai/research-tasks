# test_final_state.py

import pytest
import requests
import sqlite3
import os

API_URL = "http://127.0.0.1:8055/query"
TOKEN = "secr3t_T0k3n_99"

def test_database_exists_and_schema():
    """Verify that the SQLite database is created and has the correct schema."""
    db_path = "/home/user/processed.db"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sensor_data';")
    assert cursor.fetchone() is not None, "Table 'sensor_data' does not exist in the database."

    # Check columns
    cursor.execute("PRAGMA table_info(sensor_data);")
    columns = {row[1]: row[2] for row in cursor.fetchall()}
    assert "time_bucket" in columns, "Column 'time_bucket' missing."
    assert "sensor_id" in columns, "Column 'sensor_id' missing."
    assert "avg_value" in columns, "Column 'avg_value' missing."

    conn.close()

def test_api_unauthorized():
    """Verify that the API returns 401 when no token or incorrect token is provided."""
    try:
        response = requests.get(f"{API_URL}?sensor_id=S1", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized without token, got {response.status_code}."

    try:
        response = requests.get(f"{API_URL}?sensor_id=S1", headers={"Authorization": "Bearer wrong_token"}, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized with wrong token, got {response.status_code}."

def test_api_authorized_and_data_correct():
    """Verify that the API returns the correct aggregated data for S1."""
    headers = {"Authorization": f"Bearer {TOKEN}"}
    try:
        response = requests.get(f"{API_URL}?sensor_id=S1", headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("API response is not valid JSON.")

    assert isinstance(data, list), "Expected response to be a JSON array."

    expected_data = [
        {"time": "2023-10-01 10:00:00", "value": 16.75},
        {"time": "2023-10-01 10:15:00", "value": 30.0}
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} records, got {len(data)}."

    for i, expected in enumerate(expected_data):
        assert "time" in data[i], f"Record {i} missing 'time' key."
        assert "value" in data[i], f"Record {i} missing 'value' key."
        assert data[i]["time"] == expected["time"], f"Expected time {expected['time']}, got {data[i]['time']}."
        assert abs(data[i]["value"] - expected["value"]) < 1e-5, f"Expected value {expected['value']}, got {data[i]['value']}."