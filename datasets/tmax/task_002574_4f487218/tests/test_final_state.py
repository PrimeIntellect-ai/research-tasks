# test_final_state.py
import os
import sqlite3
import pytest

DB_PATH = "/home/user/db/time_series.db"

def test_db_exists():
    assert os.path.isfile(DB_PATH), f"Database file does not exist at {DB_PATH}"

def test_table_exists():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='readings';")
    assert cursor.fetchone() is not None, "Table 'readings' does not exist in the database."
    conn.close()

def test_schema_constraints():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check for unique index on (timestamp, device_id)
    cursor.execute("PRAGMA index_list('readings');")
    indexes = cursor.fetchall()

    is_unique = False
    for index in indexes:
        if index[2] == 1:  # unique index
            cursor.execute(f"PRAGMA index_info('{index[1]}');")
            cols = [row[2] for row in cursor.fetchall()]
            if set(cols) == {'timestamp', 'device_id'}:
                is_unique = True
                break

    # Also check if it's a composite primary key
    if not is_unique:
        cursor.execute("PRAGMA table_info('readings');")
        cols = cursor.fetchall()
        pk_cols = [col[1] for col in cols if col[5] > 0]
        if set(pk_cols) == {'timestamp', 'device_id'}:
            is_unique = True

    conn.close()
    assert is_unique, "No UNIQUE constraint or PRIMARY KEY on (timestamp, device_id) found in 'readings' table schema."

def test_data_count_and_content():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT timestamp, device_id, temperature FROM readings ORDER BY timestamp, device_id;")
    rows = cursor.fetchall()
    conn.close()

    expected_rows = [
        ("2023-10-01 10:00:00", "S1", 22.5),
        ("2023-10-01 10:00:00", "S2", 23.1),
        ("2023-10-01 10:05:00", "S1", 22.7),
        ("2023-10-01 10:05:00", "S2", 23.2),
        ("2023-10-01 10:10:00", "S1", 22.9)
    ]

    assert len(rows) == 5, f"Expected exactly 5 records (deduplicated), but got {len(rows)}."

    for actual, expected in zip(rows, expected_rows):
        assert actual == expected, f"Record mismatch. Expected {expected}, got {actual}."