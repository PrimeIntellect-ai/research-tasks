# test_final_state.py

import os
import sqlite3
import json
import hashlib
import pytest

DB_PATH = "/home/user/config_history.db"

def get_hash(state_dict):
    compact_json = json.dumps(state_dict, separators=(',', ':'), sort_keys=True)
    return hashlib.sha256(compact_json.encode('utf-8')).hexdigest()

def test_database_exists():
    """Test that the SQLite database file was created."""
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."
    assert os.path.isfile(DB_PATH), f"Path {DB_PATH} is not a file."

def test_table_schema():
    """Test that the changes table exists and has the correct schema."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='changes'")
    assert cur.fetchone() is not None, "Table 'changes' does not exist in the database."

    cur.execute("PRAGMA table_info(changes)")
    columns = {row[1]: row[2].upper() for row in cur.fetchall()}

    expected_columns = {
        "host_id": "TEXT",
        "epoch": "INTEGER",
        "state_hash": "TEXT",
        "masked_state": "TEXT"
    }

    for col, col_type in expected_columns.items():
        assert col in columns, f"Column '{col}' is missing from the 'changes' table."
        # We allow some flexibility in types, but SQLite usually preserves what was specified
        assert expected_columns[col] in columns[col], f"Column '{col}' has incorrect type. Expected {expected_columns[col]}, got {columns[col]}"

    conn.close()

def test_database_records():
    """Test that the database contains the correct deduplicated and masked records."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM changes ORDER BY epoch ASC")
    rows = cur.fetchall()

    assert len(rows) == 3, f"Expected exactly 3 records in the database, found {len(rows)}."

    # Expected derived data
    expected_data = [
        {
            "host_id": "web-01",
            "epoch": 1672574400,
            "masked_state": {"api_key": "***", "port": 80}
        },
        {
            "host_id": "db-01",
            "epoch": 1672578000,
            "masked_state": {"max_connections": 100, "password": "***"}
        },
        {
            "host_id": "web-01",
            "epoch": 1672581600,
            "masked_state": {"api_key": "***", "port": 443}
        }
    ]

    for i, expected in enumerate(expected_data):
        row = rows[i]
        assert row["host_id"] == expected["host_id"], f"Record {i+1}: Incorrect host_id. Expected {expected['host_id']}, got {row['host_id']}"
        assert row["epoch"] == expected["epoch"], f"Record {i+1}: Incorrect epoch timestamp. Expected {expected['epoch']}, got {row['epoch']}"

        # Check masked state parsing
        try:
            actual_masked_state = json.loads(row["masked_state"])
        except json.JSONDecodeError:
            pytest.fail(f"Record {i+1}: masked_state is not valid JSON.")

        assert actual_masked_state == expected["masked_state"], f"Record {i+1}: Incorrect masked_state. Expected {expected['masked_state']}, got {actual_masked_state}"

        # Check hash
        expected_hash = get_hash(expected["masked_state"])
        assert row["state_hash"] == expected_hash, f"Record {i+1}: Incorrect state_hash. Expected {expected_hash}, got {row['state_hash']}"

    conn.close()