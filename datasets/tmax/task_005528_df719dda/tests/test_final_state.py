# test_final_state.py

import os
import sqlite3

def test_database_exists():
    db_path = "/home/user/threat_activity.db"
    assert os.path.isfile(db_path), f"Database file {db_path} was not created."

def test_database_contents():
    db_path = "/home/user/threat_activity.db"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='activity_summary';")
    assert cursor.fetchone() is not None, "Table 'activity_summary' does not exist in the database."

    # Query data
    cursor.execute("SELECT bucket_time, ip, request_count FROM activity_summary ORDER BY bucket_time, ip;")
    rows = cursor.fetchall()

    expected_rows = [
        ("2023-10-01T10:00:00Z", "10.0.0.5", 3),
        ("2023-10-01T10:00:00Z", "10.0.0.9", 1),
        ("2023-10-01T10:05:00Z", "10.0.0.5", 1),
        ("2023-10-01T10:05:00Z", "10.0.0.9", 1),
        ("2023-10-01T10:10:00Z", "10.0.0.9", 1)
    ]

    assert len(rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in 'activity_summary', but got {len(rows)}."

    for i, (expected, actual) in enumerate(zip(expected_rows, rows)):
        assert expected == actual, f"Row {i+1} mismatch. Expected {expected}, got {actual}."

    conn.close()