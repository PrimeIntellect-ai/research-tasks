# test_final_state.py

import os
import sqlite3
import pytest

LOG_PATH = "/home/user/project/matched_files.log"
DB_PATH = "/home/user/project/files.db"

EXPECTED_PATHS = [
    "/home/user/project/data/a.txt",
    "/home/user/project/data/d.txt"
]

def test_matched_files_log():
    """Verify that matched_files.log exists and contains the correct sorted paths."""
    assert os.path.isfile(LOG_PATH), f"Expected log file does not exist: {LOG_PATH}"

    with open(LOG_PATH, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert lines == EXPECTED_PATHS, f"Contents of {LOG_PATH} do not match the expected sorted paths. Got: {lines}"

def test_database_exists():
    """Verify that the SQLite database file exists."""
    assert os.path.isfile(DB_PATH), f"Expected database file does not exist: {DB_PATH}"

def test_database_schema():
    """Verify that the files_v2 table exists and has the correct columns."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if table files_v2 exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='files_v2';")
    table = cursor.fetchone()
    assert table is not None, "Table 'files_v2' does not exist in the database."

    # Check columns of files_v2
    cursor.execute("PRAGMA table_info(files_v2);")
    columns = {row[1] for row in cursor.fetchall()}

    expected_columns = {"id", "path", "matched_rule"}
    assert expected_columns.issubset(columns), f"Table 'files_v2' is missing required columns. Expected at least {expected_columns}, got {columns}"

    conn.close()

def test_database_content():
    """Verify that the files_v2 table contains the correct matched paths."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT path FROM files_v2 ORDER BY path;")
        rows = cursor.fetchall()
    except sqlite3.OperationalError as e:
        pytest.fail(f"Failed to query files_v2 table: {e}")
    finally:
        conn.close()

    actual_paths = [row[0] for row in rows]
    assert actual_paths == EXPECTED_PATHS, f"Database paths do not match expected paths. Got: {actual_paths}"