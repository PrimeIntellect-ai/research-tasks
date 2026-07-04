# test_final_state.py

import os
import sqlite3
import pytest

def test_violations_log():
    log_path = "/home/user/violations.log"
    assert os.path.isfile(log_path), f"Expected file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_names = ["Bob", "Charlie", "Dave", "Eve"]
    assert lines == expected_names, f"Expected {expected_names} in violations.log, but got {lines}."

def test_go_module():
    go_mod_path = "/home/user/audit/go.mod"
    assert os.path.isfile(go_mod_path), f"Go module file {go_mod_path} does not exist."

    with open(go_mod_path, "r") as f:
        content = f.read()

    assert "github.com/mattn/go-sqlite3" in content, "go.mod does not contain the required github.com/mattn/go-sqlite3 dependency."

def test_database_indexes():
    db_path = "/home/user/audit.db"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index';")
    indexes = cursor.fetchall()
    conn.close()

    # Filter out sqlite auto-indexes
    user_indexes = [idx for idx in indexes if not idx[0].startswith("sqlite_")]

    tables_with_indexes = {idx[1] for idx in user_indexes}

    assert "group_hierarchy" in tables_with_indexes, "No index found on table 'group_hierarchy'."
    assert "group_members" in tables_with_indexes, "No index found on table 'group_members'."