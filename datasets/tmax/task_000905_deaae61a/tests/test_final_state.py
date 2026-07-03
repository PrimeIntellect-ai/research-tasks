# test_final_state.py
import os
import sqlite3
import pytest

DB_PATH = "/home/user/audit_system.db"
QUERY_PLAN_PATH = "/home/user/query_plan.txt"
C_SOURCE_PATH = "/home/user/check_compliance.c"
VIOLATIONS_LOG_PATH = "/home/user/violations.log"

def test_index_created():
    """Check if the idx_emp_access index was created on restricted_access_logs."""
    assert os.path.exists(DB_PATH), f"Database missing at {DB_PATH}"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index' AND name='idx_emp_access';")
    result = cursor.fetchone()
    conn.close()

    assert result is not None, "Index 'idx_emp_access' was not found."
    assert result[1] == 'restricted_access_logs', f"Index 'idx_emp_access' is on wrong table: {result[1]}"

def test_query_plan_file():
    """Check if the query plan file exists and contains relevant output."""
    assert os.path.exists(QUERY_PLAN_PATH), f"Query plan file missing at {QUERY_PLAN_PATH}"
    with open(QUERY_PLAN_PATH, "r") as f:
        content = f.read().upper()

    # It should look like an EXPLAIN QUERY PLAN output
    assert "SCAN" in content or "SEARCH" in content or "IDX_EMP_ACCESS" in content, \
        "The query plan file does not seem to contain a valid SQLite EXPLAIN QUERY PLAN output."

def test_c_program_exists():
    """Check if the C program source file exists."""
    assert os.path.exists(C_SOURCE_PATH), f"C source file missing at {C_SOURCE_PATH}"

def test_violations_log():
    """Check if the violations log exists and contains the exact expected violations."""
    assert os.path.exists(VIOLATIONS_LOG_PATH), f"Violations log missing at {VIOLATIONS_LOG_PATH}"

    with open(VIOLATIONS_LOG_PATH, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "Bob Jones unauthorized access to Apollo",
        "Charlie Brown unauthorized access to Zeus"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} violations, found {len(lines)}."

    for i, expected in enumerate(expected_lines):
        assert lines[i] == expected, f"Mismatch at line {i+1}. Expected: '{expected}', Got: '{lines[i]}'"