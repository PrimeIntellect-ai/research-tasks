# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = "/home/user/artifacts.db"

def test_db_file_exists():
    """Check if the SQLite database file exists."""
    assert os.path.isfile(DB_PATH), f"Database file missing at {DB_PATH}"

def test_v2_artifacts_table_exists():
    """Check if the v2_artifacts table exists in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='v2_artifacts';")
    result = cursor.fetchone()
    conn.close()
    assert result is not None, "Table 'v2_artifacts' does not exist in the database. Did you create it?"

def test_v2_artifacts_schema():
    """Check if the v2_artifacts table has the correct schema."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(v2_artifacts);")
    columns = cursor.fetchall()
    conn.close()

    # PRAGMA table_info returns: (cid, name, type, notnull, dflt_value, pk)
    column_names = [col[1] for col in columns]
    expected_columns = ["id", "project", "version", "filename", "branch", "commit_hash"]

    for expected in expected_columns:
        assert expected in column_names, f"Column '{expected}' is missing from v2_artifacts table."

def test_v2_artifacts_data():
    """Check if the v2_artifacts table contains the correctly migrated data."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, project, version, filename, branch, commit_hash FROM v2_artifacts ORDER BY id;")
    rows = cursor.fetchall()
    conn.close()

    expected_rows = [
        (1, 'frontend', 'v1.0.0', 'bundle.js', 'main', 'a3f29cd'),
        (2, 'backend', 'v2.3.1', 'server.bin', 'staging', 'b83912f'),
        (3, 'auth-service', 'v0.9.5', 'auth-linux-amd64', 'hotfix-1', 'c123456')
    ]

    assert len(rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in v2_artifacts, found {len(rows)}."
    for row, expected in zip(rows, expected_rows):
        assert row == expected, f"Row mismatch in v2_artifacts: expected {expected}, got {row}."