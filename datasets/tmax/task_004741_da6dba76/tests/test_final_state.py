# test_final_state.py

import os
import sqlite3
import re
import pytest

DB_PATH = "/home/user/fleet_data.db"
CRON_PATH = "/home/user/cron_schedule.txt"

def test_database_exists():
    """Check if the SQLite database file was created."""
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} was not created."
    assert os.path.isfile(DB_PATH), f"Path {DB_PATH} is not a file."

def test_hourly_stats_table_and_data():
    """Check if the hourly_stats table exists and contains the correct aggregated data."""
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='hourly_stats';")
        assert cursor.fetchone() is not None, "Table 'hourly_stats' does not exist in the database."

        # Check the data
        cursor.execute("SELECT bucket, vehicle_id, avg_speed, max_temp FROM hourly_stats ORDER BY vehicle_id, bucket;")
        rows = cursor.fetchall()

        expected_rows = [
            ("2023-10-01 10:00:00", "V1", 50.0, 22.0),
            ("2023-10-01 11:00:00", "V1", 60.0, 26.0),
            ("2023-10-01 10:00:00", "V2", 35.0, 19.0)
        ]

        assert len(rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, but got {len(rows)}."

        for i, (actual, expected) in enumerate(zip(rows, expected_rows)):
            assert actual[0] == expected[0], f"Row {i+1} bucket mismatch: expected {expected[0]}, got {actual[0]}"
            assert actual[1] == expected[1], f"Row {i+1} vehicle_id mismatch: expected {expected[1]}, got {actual[1]}"
            assert abs(actual[2] - expected[2]) < 1e-5, f"Row {i+1} avg_speed mismatch: expected {expected[2]}, got {actual[2]}"
            assert abs(actual[3] - expected[3]) < 1e-5, f"Row {i+1} max_temp mismatch: expected {expected[3]}, got {actual[3]}"

    except sqlite3.Error as e:
        pytest.fail(f"SQLite error occurred: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def test_cron_schedule_file():
    """Check if the cron schedule file is created and contains the correct crontab line."""
    assert os.path.exists(CRON_PATH), f"Cron schedule file {CRON_PATH} was not created."
    assert os.path.isfile(CRON_PATH), f"Path {CRON_PATH} is not a file."

    with open(CRON_PATH, "r") as f:
        content = f.read().strip()

    assert content, f"File {CRON_PATH} is empty."

    # Regex to match: 0 * * * * python3 /home/user/etl_pipeline.py
    # Allow multiple spaces, optional /usr/bin/ prefix for python3
    pattern = r"^0\s+\*\s+\*\s+\*\s+\*\s+(?:/usr/bin/)?python3\s+/home/user/etl_pipeline\.py$"

    # Check if any line matches the pattern
    lines = content.splitlines()
    match_found = any(re.match(pattern, line.strip()) for line in lines)

    assert match_found, (
        f"File {CRON_PATH} does not contain the correct cron schedule. "
        f"Expected a line matching '0 * * * * python3 /home/user/etl_pipeline.py'. "
        f"Actual content: {content}"
    )