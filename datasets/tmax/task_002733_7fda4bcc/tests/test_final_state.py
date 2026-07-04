# test_final_state.py
import os
import sqlite3
import requests
import pytest

def test_process_endpoint_and_anomalies():
    db_path = '/tmp/test_data.sqlite'

    assert os.path.exists(db_path), f"Database {db_path} does not exist."

    # Read original data to compute expected anomalies
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wide_readings ORDER BY timestamp ASC")
    rows = cursor.fetchall()

    # Get column names
    col_names = [description[0] for description in cursor.description]
    ts_idx = col_names.index('timestamp')

    expected_anomalies = []

    # For each sensor column
    for col_idx, col_name in enumerate(col_names):
        if col_name == 'timestamp':
            continue

        prev_val = None
        for row in rows:
            ts = row[ts_idx]
            val = row[col_idx]

            if val is None:
                continue

            if prev_val is None:
                diff = 0.0
            else:
                diff = val - prev_val

            if abs(diff) > 15.0:
                expected_anomalies.append((ts, col_name, diff))

            prev_val = val

    # Send request to the service
    url = "http://127.0.0.1:8000/process"
    payload = {"db_path": db_path}
    try:
        response = requests.post(url, json=payload, timeout=20)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service or request timed out: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data.get("status") == "success", f"Expected status 'success', got {data.get('status')}"

    # Check database for anomalies table
    try:
        cursor.execute("SELECT timestamp, sensor_id, diff_value FROM anomalies ORDER BY sensor_id, timestamp")
        actual_anomalies = cursor.fetchall()
    except sqlite3.OperationalError as e:
        pytest.fail(f"Failed to query 'anomalies' table: {e}")

    assert len(actual_anomalies) == len(expected_anomalies), f"Expected {len(expected_anomalies)} rows in anomalies table, got {len(actual_anomalies)}"
    assert data.get("anomalies_inserted") == len(expected_anomalies), f"Expected {len(expected_anomalies)} anomalies inserted in response, got {data.get('anomalies_inserted')}"

    # Sort both lists to compare
    expected_anomalies.sort(key=lambda x: (x[1], x[0]))
    actual_anomalies.sort(key=lambda x: (x[1], x[0]))

    for exp, act in zip(expected_anomalies, actual_anomalies):
        assert exp[0] == act[0], f"Timestamp mismatch: expected {exp[0]}, got {act[0]}"
        assert exp[1] == act[1], f"Sensor ID mismatch: expected {exp[1]}, got {act[1]}"
        assert abs(exp[2] - act[2]) < 1e-4, f"Diff value mismatch: expected {exp[2]}, got {act[2]}"

    conn.close()