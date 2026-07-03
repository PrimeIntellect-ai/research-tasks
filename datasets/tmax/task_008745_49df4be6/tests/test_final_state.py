# test_final_state.py

import os
import sqlite3
import pytest

def test_vulnerabilities_file():
    """Test that vulnerabilities.txt contains the correct output."""
    path = "/home/user/vulnerabilities.txt"
    assert os.path.isfile(path), f"{path} does not exist. The script must create this file."

    with open(path, "r") as f:
        content = [line.strip() for line in f.read().strip().splitlines() if line.strip()]

    assert content == ["db_users"], f"vulnerabilities.txt contains incorrect entities. Expected ['db_users'], got {content}"

def test_indexes_created():
    """Test that optimal indexes were created on the tables."""
    db_path = "/home/user/architecture.db"
    assert os.path.isfile(db_path), f"{db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA index_list('relations');")
    relations_indexes = cursor.fetchall()
    assert len(relations_indexes) > 0, "No indexes found on the 'relations' table. You must create an index to optimize the query."

    cursor.execute("PRAGMA index_list('entities');")
    entities_indexes = cursor.fetchall()
    # Exclude auto-generated indexes for PRIMARY KEY
    custom_indexes = [idx for idx in entities_indexes if not idx[1].startswith('sqlite_autoindex_')]
    assert len(custom_indexes) > 0, "No custom indexes found on the 'entities' table. You must create an index to optimize the query."

    conn.close()

def test_query_plan_file():
    """Test that query_plan.txt exists and demonstrates index usage."""
    path = "/home/user/query_plan.txt"
    assert os.path.isfile(path), f"{path} does not exist. The script must save the EXPLAIN QUERY PLAN output."

    with open(path, "r") as f:
        content = f.read().upper()

    assert "SEARCH" in content or "USING INDEX" in content or "COVERING INDEX" in content, \
        "query_plan.txt does not demonstrate index usage. Expected to see 'SEARCH' or index scans in the plan."

def test_audit_script_exists():
    """Test that the audit.py script was created."""
    path = "/home/user/audit.py"
    assert os.path.isfile(path), f"{path} does not exist. You must write your code in this file."