# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = "/home/user/research.db"
LOG_PATH = "/home/user/result.log"
SCRIPT_PATH = "/home/user/organize_and_deadlock.py"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script missing: {SCRIPT_PATH}"

def test_database_exists_and_schema():
    assert os.path.isfile(DB_PATH), f"Database missing: {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cursor.fetchall()}
    assert "researchers" in tables, "Table 'researchers' is missing in the database"
    assert "experiments" in tables, "Table 'experiments' is missing in the database"

    # Check data in researchers
    cursor.execute("SELECT id, name FROM researchers ORDER BY id")
    researchers = cursor.fetchall()
    assert researchers == [(1, "Alice"), (2, "Bob")], "Data in 'researchers' table is incorrect"

    # Check data in experiments
    cursor.execute("SELECT id, researcher_id FROM experiments ORDER BY id")
    experiments = cursor.fetchall()
    assert experiments == [(101, 1), (102, 2)], "Data in 'experiments' table is incorrect"

    # Check index
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='experiments'")
    indexes = cursor.fetchall()
    assert len(indexes) > 0, "No index found on 'experiments' table to optimize the query"

    conn.close()

def test_result_log():
    assert os.path.isfile(LOG_PATH), f"Log file missing: {LOG_PATH}"

    with open(LOG_PATH, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {LOG_PATH}, found {len(lines)}"

    plan_line = lines[0]
    deadlock_line = lines[1]

    assert plan_line.startswith("PLAN:"), "First line must start with 'PLAN:'"
    assert "SEARCH" in plan_line.upper() or "SCAN" in plan_line.upper(), "First line should contain the query plan details"
    assert "INDEX" in plan_line.upper(), "Query plan should indicate the use of an index"

    assert deadlock_line == "DEADLOCK_ACHIEVED", "Second line must be exactly 'DEADLOCK_ACHIEVED'"