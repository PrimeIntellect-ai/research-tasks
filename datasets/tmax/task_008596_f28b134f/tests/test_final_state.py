# test_final_state.py
import os
import json
import sqlite3
import pytest

def test_db_exists_and_table_populated():
    """Test that the SQLite database exists and the lock_events table is populated."""
    db_path = '/home/user/etl.db'
    assert os.path.isfile(db_path), f"Database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='lock_events'")
    table = cursor.fetchone()
    assert table is not None, "Table 'lock_events' does not exist in the database."

    cursor.execute("SELECT COUNT(*) FROM lock_events")
    count = cursor.fetchone()[0]
    assert count > 0, "Table 'lock_events' is empty."
    conn.close()

def test_indexes_created():
    """Test that at least one index was created on the lock_events table."""
    db_path = '/home/user/etl.db'
    assert os.path.isfile(db_path), f"Database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='lock_events'")
    indexes = cursor.fetchall()

    # Exclude auto-created indexes (like sqlite_autoindex) if any
    user_indexes = [idx[0] for idx in indexes if not idx[0].startswith('sqlite_')]
    assert len(user_indexes) > 0, "No indexes found on 'lock_events' table."
    conn.close()

def test_report_json_correctness():
    """Test that the report.json file exists, is valid JSON, and contains the correct results."""
    report_path = '/home/user/report.json'
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, 'r') as f:
        try:
            result = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    expected = {
      "top_blockers": [
        {"rank": 1, "tx_id": 1, "blocking_score": 2},
        {"rank": 2, "tx_id": 4, "blocking_score": 2},
        {"rank": 3, "tx_id": 6, "blocking_score": 1},
        {"rank": 4, "tx_id": 2, "blocking_score": 0},
        {"rank": 5, "tx_id": 3, "blocking_score": 0}
      ]
    }

    assert result == expected, f"Report JSON content mismatch.\nExpected: {expected}\nGot: {result}"