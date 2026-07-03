# test_final_state.py

import os
import sqlite3
import hashlib
import pytest

DB_PATH = "/home/user/data/measurements.db"

def test_db_exists():
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} was not created."

def test_table_schema():
    assert os.path.isfile(DB_PATH), "Database missing, cannot check schema."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if table metrics exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='metrics';")
    assert cursor.fetchone() is not None, "Table 'metrics' does not exist in the database."

    # Check schema
    cursor.execute("PRAGMA table_info(metrics);")
    columns = {row[1]: row[2].upper() for row in cursor.fetchall()}

    expected_columns = {
        "hash": "TEXT",
        "timestamp": "TEXT",
        "sensor_id": "TEXT",
        "metric_type": "TEXT",
        "value": "REAL"
    }

    for col, col_type in expected_columns.items():
        assert col in columns, f"Column '{col}' is missing from the 'metrics' table."
        # SQLite types might vary slightly (e.g., TEXT vs VARCHAR), but standardizing on TEXT/REAL
        assert expected_columns[col] in columns[col], f"Column '{col}' should be of type {expected_columns[col]}, found {columns[col]}."

    conn.close()

def test_data_content():
    assert os.path.isfile(DB_PATH), "Database missing, cannot check data."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT hash, timestamp, sensor_id, metric_type, value FROM metrics;")
    rows = cursor.fetchall()
    conn.close()

    assert len(rows) == 4, f"Expected exactly 4 rows in the 'metrics' table, found {len(rows)}."

    expected_data = [
        ("2023-10-01T10:00:00Z", "s1", "temp", 22.5),
        ("2023-10-01T10:02:00Z", "s2", "hum", 45.0),
        ("2023-10-01T10:00:00Z", "s1", "hum", 40.0),
        ("2023-10-01T10:05:00Z", "s1", "temp", 23.0)
    ]

    # Compute expected hashes and build a dictionary for easy lookup
    expected_records = {}
    for ts, sid, mtype, val in expected_data:
        concat_str = f"{ts}{sid}{mtype}"
        h = hashlib.md5(concat_str.encode('utf-8')).hexdigest()
        expected_records[h] = (ts, sid, mtype, val)

    actual_records = {row[0]: (row[1], row[2], row[3], row[4]) for row in rows}

    for expected_hash, expected_tuple in expected_records.items():
        assert expected_hash in actual_records, f"Missing expected row with hash {expected_hash} (data: {expected_tuple}). Deduplication or hashing logic might be incorrect."

        actual_tuple = actual_records[expected_hash]
        assert actual_tuple == expected_tuple, f"Data mismatch for hash {expected_hash}. Expected {expected_tuple}, found {actual_tuple}."