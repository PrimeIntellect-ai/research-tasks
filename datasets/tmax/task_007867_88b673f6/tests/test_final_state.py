# test_final_state.py

import os
import json
import sqlite3
import pytest

DB_PATH = '/home/user/sensor_data.db'
JSON_PATH = '/home/user/quarantine.json'

def test_database_exists():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} not found."
    assert os.path.isfile(DB_PATH), f"{DB_PATH} is not a file."

def test_database_schema_and_content():
    assert os.path.exists(DB_PATH), "Database missing"
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Check table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='readings'")
    assert c.fetchone() is not None, "Table 'readings' does not exist in the database."

    # Check schema
    c.execute("PRAGMA table_info(readings)")
    columns = {row[1]: row[2].upper() for row in c.fetchall()}

    expected_columns = {
        'sensor_id': 'TEXT',
        'timestamp': 'TEXT',
        'temperature': 'REAL',
        'humidity': 'REAL',
        'status': 'TEXT'
    }

    for col, ctype in expected_columns.items():
        assert col in columns, f"Column '{col}' missing from readings table."
        # We don't strictly assert the type since SQLite is flexible, but having the column is required.

    # Check row count
    c.execute("SELECT count(*) FROM readings")
    db_count = c.fetchone()[0]
    assert db_count == 3, f"Expected exactly 3 valid rows in the database, got {db_count}."

    # Verify the contents of the valid rows
    c.execute("SELECT sensor_id, timestamp, temperature, humidity, status FROM readings ORDER BY timestamp")
    rows = c.fetchall()

    expected_rows = [
        ("SN-1234", "2023-10-01T10:00:00Z", 22.5, 45.0, "ACTIVE"),
        ("SN-0001", "2023-10-01T10:20:00Z", 0.0, 0.0, "OFFLINE"),
        ("SN-5555", "2023-10-02T10:10:00Z", 85.0, 100.0, "MAINTENANCE")
    ]

    for expected, actual in zip(expected_rows, rows):
        assert actual == expected, f"Expected row {expected}, got {actual}."

    conn.close()

def test_quarantine_json_exists():
    assert os.path.exists(JSON_PATH), f"Quarantine JSON file {JSON_PATH} not found."
    assert os.path.isfile(JSON_PATH), f"{JSON_PATH} is not a file."

def test_quarantine_json_content():
    assert os.path.exists(JSON_PATH), "JSON missing"
    with open(JSON_PATH, 'r') as f:
        try:
            q_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {JSON_PATH} is not valid JSON.")

    assert isinstance(q_data, list), "Quarantine JSON should contain a single JSON array."
    assert len(q_data) == 5, f"Expected exactly 5 invalid rows in JSON, got {len(q_data)}."

    for row in q_data:
        assert "invalid_columns" in row, "Each object must contain an 'invalid_columns' key."
        cols = row["invalid_columns"]
        assert isinstance(cols, list), "'invalid_columns' must be a list of strings."
        assert cols == sorted(cols), f"'invalid_columns' must be sorted alphabetically. Got: {cols}"

        # Verify specific failure reasons based on the input data
        if row.get("temperature") == "100.0":
            assert cols == ["temperature"], f"Expected ['temperature'] for row with temp 100.0, got {cols}"
        elif row.get("sensor_id") == "S-123":
            assert cols == ["sensor_id", "status"], f"Expected ['sensor_id', 'status'] for S-123, got {cols}"
        elif row.get("temperature") == "-45.0":
            assert cols == ["humidity", "temperature"], f"Expected ['humidity', 'temperature'] for temp -45.0, got {cols}"
        elif row.get("temperature") == "abc":
            assert cols == ["temperature"], f"Expected ['temperature'] for temp 'abc', got {cols}"
        elif row.get("timestamp") == "2023-10-02 10:05:00Z":
            assert cols == ["timestamp"], f"Expected ['timestamp'] for invalid timestamp format, got {cols}"
        else:
            pytest.fail(f"Unexpected row found in quarantine JSON: {row}")