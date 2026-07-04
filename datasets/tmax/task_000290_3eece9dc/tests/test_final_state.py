# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = "/home/user/incidents.db"

def test_database_exists():
    """Test that the SQLite database was created at the correct location."""
    assert os.path.isfile(DB_PATH), f"Database file not found at {DB_PATH}"

def test_table_schema():
    """Test that the 'errors' table exists and has the correct columns."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Check if table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='errors'")
    table = c.fetchone()
    assert table is not None, "Table 'errors' does not exist in the database."

    # Check columns
    c.execute("PRAGMA table_info(errors)")
    columns_info = c.fetchall()

    # PRAGMA table_info returns: (cid, name, type, notnull, dflt_value, pk)
    column_names = [col[1] for col in columns_info]
    expected_columns = ["timestamp", "ip", "endpoint", "status"]

    for col in expected_columns:
        assert col in column_names, f"Column '{col}' is missing from the 'errors' table."

    conn.close()

def test_database_records():
    """Test that the 'errors' table contains exactly the expected records (status >= 400)."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT count(*) FROM errors")
    count = c.fetchone()[0]
    assert count == 4, f"Expected 4 error records in the 'errors' table, got {count}."

    c.execute("SELECT timestamp, ip, endpoint, status FROM errors ORDER BY timestamp ASC")
    rows = c.fetchall()

    expected = [
        ("2023-10-14T12:01:15Z", "10.0.0.5", "/api/v1/auth", 401),
        ("2023-10-14T12:03:05Z", "172.16.0.4", "/admin/config", 403),
        ("2023-10-14T12:04:50Z", "10.0.0.8", "/api/v1/missing", 404),
        ("2023-10-14T12:05:10Z", "192.168.1.105", "/api/v1/status", 500)
    ]

    assert rows == expected, f"Expected records {expected}, but got {rows}."

    conn.close()