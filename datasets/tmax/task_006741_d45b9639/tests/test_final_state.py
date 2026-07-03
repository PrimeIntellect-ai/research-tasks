# test_final_state.py

import os
import sqlite3
import pytest

PIPELINE_DIR = "/home/user/pipeline"
DB_PATH = os.path.join(PIPELINE_DIR, "db.sqlite")
SUCCESS_LOG_PATH = os.path.join(PIPELINE_DIR, "success.log")

def test_success_log():
    assert os.path.isfile(SUCCESS_LOG_PATH), f"The file {SUCCESS_LOG_PATH} does not exist. Did you run build.sh successfully?"

    with open(SUCCESS_LOG_PATH, "r") as f:
        content = f.read().strip()

    assert content == "Auth Check: 1", f"Expected success.log to contain exactly 'Auth Check: 1', but found: '{content}'"

def test_sqlite_schema():
    assert os.path.isfile(DB_PATH), f"SQLite database {DB_PATH} is missing."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(sessions);")
    columns = {row[1]: row[2] for row in cursor.fetchall()}

    assert "expiry" in columns, "The 'expiry' column is missing from the 'sessions' table."
    assert "INTEGER" in columns["expiry"].upper(), f"The 'expiry' column should be of type INTEGER, but found {columns['expiry']}."

    conn.close()