# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = "/home/user/dataset.db"
RESULT_PATH = "/home/user/result.txt"
C_FILE_PATH = "/home/user/fix_and_analyze.c"

def test_c_file_exists():
    """Test that the C program file exists."""
    assert os.path.isfile(C_FILE_PATH), f"C file missing at {C_FILE_PATH}"

def test_result_file_content():
    """Test that the result file exists and contains the correct output."""
    assert os.path.isfile(RESULT_PATH), f"Result file missing at {RESULT_PATH}"

    with open(RESULT_PATH, 'r') as f:
        content = f.read().strip()

    expected_content = "Top Node: 42, Degree: 5"
    assert content == expected_content, f"Expected result file content to be '{expected_content}', but got '{content}'"

def test_database_indexes():
    """Test that the stale index was dropped and the fresh index was created."""
    assert os.path.isfile(DB_PATH), f"Database file missing at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check that idx_stale is dropped
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_stale';")
    stale_index = cursor.fetchone()
    assert stale_index is None, "Index 'idx_stale' was not dropped."

    # Check that idx_fresh is created
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_fresh';")
    fresh_index = cursor.fetchone()
    assert fresh_index is not None, "Index 'idx_fresh' was not created."

    # Verify idx_fresh is on the target column
    cursor.execute("PRAGMA index_info('idx_fresh');")
    columns = [row[2] for row in cursor.fetchall()]
    assert 'target' in columns, "Index 'idx_fresh' is not on the 'target' column."

    conn.close()