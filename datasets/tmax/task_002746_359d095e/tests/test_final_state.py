# test_final_state.py

import os
import sqlite3
import pytest
import requests
import time
import subprocess

DB_PATH = "/home/user/app/data/research.db"
SERVER_URL = "http://127.0.0.1:8080/api/v1/stats"

def test_database_integrity_and_index():
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} is missing"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if idx_time exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_time';")
    assert cursor.fetchone() is not None, "Index 'idx_time' is missing"

    # Check integrity to ensure the index is not corrupted
    cursor.execute("PRAGMA integrity_check;")
    result = cursor.fetchone()[0]
    assert result == "ok", f"Database integrity check failed: {result}"

    conn.close()

def test_services_running():
    # Check if ingestor is running
    try:
        ps_output = subprocess.check_output(["ps", "aux"]).decode("utf-8")
    except subprocess.CalledProcessError:
        pytest.fail("Failed to execute ps aux")

    assert "ingestor.py" in ps_output, "ingestor.py is not running"
    assert "./server" in ps_output or "server" in ps_output, "C++ server is not running"

def test_api_endpoint():
    # Wait a moment in case the server is just starting
    time.sleep(1)

    try:
        response = requests.get(f"{SERVER_URL}?exp_id=1", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the C++ server: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert "application/json" in response.headers.get("Content-Type", ""), "Expected Content-Type application/json"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    assert "schema_version" in data, "Missing 'schema_version' in response"
    assert data["schema_version"] == "1.0", f"Expected schema_version '1.0', got {data['schema_version']}"

    assert "data" in data, "Missing 'data' in response"
    assert isinstance(data["data"], list), "'data' should be a list"

    measurements = data["data"]
    if not measurements:
        # If the ingestor hasn't inserted anything for exp_id=1, we can't fully test math, 
        # but the setup says it inserts dummy data.
        pytest.fail("No data returned for exp_id=1, expected at least some measurements.")

    running_sum = 0.0
    count = 0
    last_timestamp = None

    for row in measurements:
        assert "id" in row, "Missing 'id' in row"
        assert "timestamp" in row, "Missing 'timestamp' in row"
        assert "sensor_value" in row, "Missing 'sensor_value' in row"
        assert "cumulative_avg" in row, "Missing 'cumulative_avg' in row"

        # Check ordering
        if last_timestamp is not None:
            assert row["timestamp"] >= last_timestamp, "Results are not ordered by timestamp ascending"
        last_timestamp = row["timestamp"]

        # Check math
        val = float(row["sensor_value"])
        running_sum += val
        count += 1
        expected_avg = running_sum / count

        actual_avg = float(row["cumulative_avg"])
        assert abs(actual_avg - expected_avg) < 1e-5, f"Incorrect cumulative_avg at id {row['id']}: expected {expected_avg}, got {actual_avg}"