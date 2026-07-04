# test_final_state.py

import os
import re
import pytest

def test_audit_success_log():
    """Verify that the C++ tool executed successfully and created the log file."""
    log_path = "/home/user/audit_tool/audit_success.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing. Did the C++ program run successfully?"

    with open(log_path, "r") as f:
        content = f.read().strip()
    assert "AUDIT_COMPLETE" in content, f"Expected 'AUDIT_COMPLETE' in {log_path}, but found: {content}"

def test_optimize_sql():
    """Verify that the optimization SQL script exists and contains a CREATE INDEX statement."""
    sql_path = "/home/user/optimize.sql"
    assert os.path.isfile(sql_path), f"SQL script {sql_path} is missing."

    with open(sql_path, "r") as f:
        content = f.read()

    assert re.search(r"CREATE\s+(UNIQUE\s+)?INDEX", content, re.IGNORECASE), \
        f"{sql_path} does not contain a CREATE INDEX statement."
    assert re.search(r"transactions", content, re.IGNORECASE), \
        f"{sql_path} does not seem to create an index on the 'transactions' table."

def test_path_sql_exists():
    """Verify that the path.sql script exists."""
    sql_path = "/home/user/path.sql"
    assert os.path.isfile(sql_path), f"SQL script {sql_path} is missing."

def test_shortest_path_csv():
    """Verify that the shortest path CSV exists and contains the correct path length."""
    csv_path = "/home/user/shortest_path.csv"
    assert os.path.isfile(csv_path), f"Output file {csv_path} is missing."

    with open(csv_path, "r") as f:
        content = f.read().strip()

    # The shortest path from 101 to 205 is 101 -> 999 -> 205, which is 2 edges.
    assert content == "2", f"Expected shortest path length to be '2', but found: '{content}'"