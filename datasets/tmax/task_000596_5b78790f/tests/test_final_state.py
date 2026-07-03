# test_final_state.py
import os
import sqlite3
import pytest

DB_PATH = "/home/user/data.db"

def test_rolling_stats_table_exists():
    assert os.path.isfile(DB_PATH), f"The database file {DB_PATH} is missing."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='rolling_stats';")
    assert cursor.fetchone() is not None, "Table 'rolling_stats' was not created in the database."
    conn.close()

def test_rolling_stats_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if we can select the required columns
    try:
        cursor.execute("SELECT user_id, username, event_date, rolling_avg FROM rolling_stats ORDER BY user_id ASC, event_date ASC;")
        rows = cursor.fetchall()
    except sqlite3.OperationalError as e:
        pytest.fail(f"Failed to query 'rolling_stats': {e}")
    finally:
        conn.close()

    expected_data = [
        (1, 'alice', '2023-01-01', 10.0),
        (1, 'alice', '2023-01-03', 15.0),
        (1, 'alice', '2023-01-05', 20.0),
        (1, 'alice', '2023-01-07', 30.0),
        (2, 'bob', '2023-01-02', 15.0),
        (2, 'bob', '2023-01-04', 20.0),
        (2, 'bob', '2023-01-06', 15.0)
    ]

    assert len(rows) == len(expected_data), f"Expected {len(expected_data)} rows in rolling_stats, found {len(rows)}."

    for i, (actual, expected) in enumerate(zip(rows, expected_data)):
        assert actual[0] == expected[0], f"Row {i+1}: expected user_id {expected[0]}, got {actual[0]}"
        assert actual[1] == expected[1], f"Row {i+1}: expected username {expected[1]}, got {actual[1]}"
        assert actual[2] == expected[2], f"Row {i+1}: expected event_date {expected[2]}, got {actual[2]}"
        # Allow small floating point differences, though it should be exactly rounded to 2 decimal places
        assert abs(actual[3] - expected[3]) < 1e-5, f"Row {i+1}: expected rolling_avg {expected[3]}, got {actual[3]}"

def test_original_tables_unmodified():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users;")
    user_count = cursor.fetchone()[0]
    assert user_count == 2, f"Expected 2 users to remain, found {user_count}"

    cursor.execute("SELECT COUNT(*) FROM events;")
    event_count = cursor.fetchone()[0]
    assert event_count == 7, f"Expected 7 events to remain, found {event_count}"

    conn.close()