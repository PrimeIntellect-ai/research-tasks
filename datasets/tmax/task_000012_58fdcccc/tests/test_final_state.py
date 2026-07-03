# test_final_state.py

import os
import sqlite3
import json
import pytest

DB_PATH = "/home/user/climate_data.db"
REPORT_PATH = "/home/user/alpine_temp_report.json"

def test_indexes_created():
    assert os.path.exists(DB_PATH), f"Database file missing at {DB_PATH}"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Query for user-created indexes (excluding sqlite's internal auto-indexes)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_autoindex%';")
    indexes = cursor.fetchall()
    conn.close()

    assert len(indexes) >= 2, f"Expected at least 2 user-created indexes, but found {len(indexes)}: {indexes}"

def test_report_json_correct():
    assert os.path.exists(REPORT_PATH), f"Report file missing at {REPORT_PATH}"

    # Compute the expected result directly from the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = """
    SELECT r.sensor_id, r.timestamp, r.value,
           ROUND(AVG(r.value) OVER (
               PARTITION BY r.sensor_id 
               ORDER BY r.timestamp 
               ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
           ), 2) as moving_avg
    FROM readings r
    JOIN sensors s ON r.sensor_id = s.id
    JOIN locations l ON s.location_id = l.id
    WHERE s.type = 'TEMP' AND l.region_name = 'Alpine_Zone'
    ORDER BY r.sensor_id ASC, r.timestamp ASC
    """
    rows = cursor.execute(query).fetchall()
    conn.close()

    expected_result = []
    for row in rows:
        expected_result.append({
            "sensor_id": row[0],
            "timestamp": row[1],
            "value": row[2],
            "moving_avg": row[3]
        })

    with open(REPORT_PATH, 'r') as f:
        try:
            actual_result = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} does not contain valid JSON.")

    assert actual_result == expected_result, "The generated JSON report does not match the expected output."