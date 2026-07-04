# test_final_state.py

import os
import sqlite3
import pytest

REPORT_PATH = "/home/user/deadlock_report.txt"
DB_PATH = "/home/user/audit.db"

def test_deadlock_report_content():
    """Check if the deadlock report contains the correct deadlocked transactions."""
    assert os.path.isfile(REPORT_PATH), f"Report file missing at {REPORT_PATH}"

    with open(REPORT_PATH, 'r') as f:
        content = f.read().strip()

    assert content == "1001,1002,1003", f"Expected '1001,1002,1003' in {REPORT_PATH}, got '{content}'"

def test_database_index_exists():
    """Check if the idx_locks index was created in the database."""
    assert os.path.isfile(DB_PATH), f"Database file missing at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_locks';")
    result = cursor.fetchone()

    conn.close()

    assert result is not None, "Index 'idx_locks' was not found in the database."
    assert result[0] == "idx_locks", "Index 'idx_locks' was not found in the database."