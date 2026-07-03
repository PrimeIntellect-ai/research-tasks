# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = '/home/user/data/sensors.db'

def get_db_connection():
    assert os.path.isfile(DB_PATH), f"Database file missing at {DB_PATH}"
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def test_database_exists():
    assert os.path.isfile(DB_PATH), f"Database file not found at {DB_PATH}"

def test_table_schema_and_row_count():
    conn = get_db_connection()
    c = conn.cursor()

    # Check if table 'readings' exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='readings'")
    assert c.fetchone() is not None, "Table 'readings' does not exist in the database."

    # Check columns
    c.execute("PRAGMA table_info(readings)")
    columns = {row['name'] for row in c.fetchall()}
    expected_columns = {'sensor_id', 'timestamp', 'temperature', 'notes', 'is_anomaly'}
    assert expected_columns.issubset(columns), f"Table 'readings' is missing expected columns. Found: {columns}"

    # Check row count
    c.execute("SELECT COUNT(*) as cnt FROM readings")
    count = c.fetchone()['cnt']
    assert count == 5, f"Expected 5 rows in 'readings' table, found {count}."

    conn.close()

def test_timestamps_and_anomalies():
    conn = get_db_connection()
    c = conn.cursor()

    # Expected data: (sensor_id, timestamp, is_anomaly)
    expected_data = [
        ('S1', '2023-10-01T14:00:00Z', 0),
        ('S1', '2023-10-01T14:30:00Z', 1),
        ('S1', '2023-10-01T16:00:00Z', 0),
        ('S2', '2023-10-01T14:05:00Z', 0),
        ('S2', '2023-10-01T15:10:00Z', 0),
    ]

    for sensor_id, timestamp, expected_anomaly in expected_data:
        c.execute(
            "SELECT is_anomaly FROM readings WHERE sensor_id=? AND timestamp=?",
            (sensor_id, timestamp)
        )
        row = c.fetchone()
        assert row is not None, f"Missing reading for sensor {sensor_id} at {timestamp}. Check timestamp formatting and UTC conversion."

        # is_anomaly might be stored as boolean or integer
        anomaly_val = int(row['is_anomaly'])
        assert anomaly_val == expected_anomaly, f"Expected is_anomaly={expected_anomaly} for {sensor_id} at {timestamp}, got {anomaly_val}."

    conn.close()

def test_embedded_newline_in_notes():
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("SELECT notes FROM readings WHERE sensor_id='S2' AND timestamp='2023-10-01T14:05:00Z'")
    row = c.fetchone()
    assert row is not None, "Missing reading for S2 at 2023-10-01T14:05:00Z"

    notes = row['notes']
    assert "\n" in notes, f"Expected embedded newline in notes for S2 at 14:05:00Z, but got: {repr(notes)}. CSV parsing may have dropped or corrupted the row."

    conn.close()