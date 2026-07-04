# test_final_state.py

import os
import sqlite3
import requests
import pytest
import csv
import math

def test_cleaned_logs_csv():
    csv_path = "/home/user/cleaned_logs.csv"
    assert os.path.exists(csv_path), f"Cleaned logs file missing: {csv_path}"

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        assert headers is not None, "CSV is empty or missing headers"
        expected_headers = ["timestamp", "ip_address", "response_time", "cpu_load", "rolling_resp", "alert"]
        for h in expected_headers:
            assert h in headers, f"Missing header '{h}' in cleaned_logs.csv"

        rows = list(reader)
        assert len(rows) == 8, f"Expected 8 valid rows, found {len(rows)}"

        timestamps = [int(r["timestamp"]) for r in rows]
        assert timestamps == [0, 1, 2, 4, 5, 7, 8, 9], f"Unexpected timestamps in CSV: {timestamps}"

def test_sqlite_database():
    db_path = "/home/user/logs.db"
    assert os.path.exists(db_path), f"Database file missing: {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='metrics'")
    table_exists = cursor.fetchone()
    assert table_exists, "Table 'metrics' missing in logs.db"

    cursor.execute("SELECT timestamp, alert FROM metrics ORDER BY CAST(timestamp AS INTEGER)")
    rows = cursor.fetchall()
    assert len(rows) == 8, f"Expected 8 rows in metrics table, found {len(rows)}"

    alerts = [int(r[0]) for r in rows if int(r[1]) == 1]
    assert alerts == [2, 7], f"Expected alerts at timestamps [2, 7], found {alerts}"

    conn.close()

def test_api_alerts():
    url = "http://127.0.0.1:8000/alerts"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON: {response.text}")

    assert isinstance(data, list), "Expected a JSON array for /alerts"
    assert sorted(data) == [2, 7], f"Expected alerts [2, 7], got {data}"

def test_api_stats():
    url = "http://127.0.0.1:8000/stats"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON: {response.text}")

    assert isinstance(data, dict), "Expected a JSON object for /stats"

    expected_stats = {
        "0": 100.0,
        "1": 125.0,
        "2": 150.0,
        "4": 156.67,
        "5": 150.0,
        "7": 143.33,
        "8": 156.67,
        "9": 160.0
    }

    for ts, expected_val in expected_stats.items():
        assert ts in data, f"Missing timestamp '{ts}' in /stats response"
        val = data[ts]
        assert math.isclose(float(val), expected_val, rel_tol=1e-2), f"Expected rolling_resp for {ts} to be ~{expected_val}, got {val}"