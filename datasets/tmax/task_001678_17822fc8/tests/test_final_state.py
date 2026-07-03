# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = "/home/user/comms.db"
FLAGGED_USER_PATH = "/home/user/flagged_user.txt"
ANALYZER_GO_PATH = "/home/user/analyzer.go"

def test_flagged_user_output():
    """Verify that flagged_user.txt exists and contains the correct sender_id."""
    assert os.path.exists(FLAGGED_USER_PATH), f"Output file not found at {FLAGGED_USER_PATH}"

    with open(FLAGGED_USER_PATH, 'r') as f:
        content = f.read().strip()

    assert content == "42", f"Expected flagged_user.txt to contain '42', but got '{content}'"

def test_index_created():
    """Verify that the composite index idx_dept_time was created correctly."""
    assert os.path.exists(DB_PATH), f"Database file missing: {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if index exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_dept_time';")
    index = cursor.fetchone()
    assert index is not None, "Index 'idx_dept_time' was not found in the database."

    # Check index columns
    cursor.execute("PRAGMA index_info('idx_dept_time');")
    columns = cursor.fetchall()

    # PRAGMA index_info returns: (seqno, cid, name)
    # We expect seqno 0 to be 'department' and seqno 1 to be 'timestamp'
    assert len(columns) >= 2, "Index 'idx_dept_time' does not have enough columns."

    col_names = [col[2] for col in sorted(columns, key=lambda x: x[0])]

    assert col_names[0] == "department", f"Expected first column in index to be 'department', got '{col_names[0]}'"
    assert col_names[1] == "timestamp", f"Expected second column in index to be 'timestamp', got '{col_names[1]}'"

    conn.close()

def test_go_script_exists():
    """Verify that the Go script was created at the specified path."""
    assert os.path.exists(ANALYZER_GO_PATH), f"Go script not found at {ANALYZER_GO_PATH}"
    assert os.path.isfile(ANALYZER_GO_PATH), f"Path {ANALYZER_GO_PATH} is not a file"