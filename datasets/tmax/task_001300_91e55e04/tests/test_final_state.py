# test_final_state.py
import os
import sqlite3
import pytest

def test_optimize_sql_exists():
    assert os.path.exists("/home/user/optimize.sql"), "The file /home/user/optimize.sql is missing."
    with open("/home/user/optimize.sql", "r") as f:
        content = f.read().upper()
    assert "CREATE INDEX" in content, "/home/user/optimize.sql does not contain CREATE INDEX statements."

def test_indexes_applied_to_db():
    conn = sqlite3.connect("/home/user/audit.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name IN ('employees', 'messages')")
    indexes = cursor.fetchall()
    conn.close()
    assert len(indexes) > 0, "No indexes were applied to the employees or messages tables in audit.db."

def test_query_plan_extracted():
    assert os.path.exists("/home/user/query_plan.txt"), "The file /home/user/query_plan.txt is missing."
    with open("/home/user/query_plan.txt", "r") as f:
        content = f.read()
    assert len(content.strip()) > 0, "The query_plan.txt file is empty."
    # The output of EXPLAIN QUERY PLAN usually contains keywords like SCAN, SEARCH, or USING INDEX
    assert any(keyword in content.upper() for keyword in ["SCAN", "SEARCH", "USING INDEX", "COVERING INDEX"]), \
        "The query_plan.txt file does not appear to contain valid EXPLAIN QUERY PLAN output."

def test_audit_tool_compiled():
    assert os.path.exists("/home/user/audit_tool"), "The compiled binary /home/user/audit_tool is missing."
    assert os.access("/home/user/audit_tool", os.X_OK), "The file /home/user/audit_tool is not executable."

def test_highest_centrality():
    assert os.path.exists("/home/user/highest_centrality.txt"), "The file /home/user/highest_centrality.txt is missing."
    with open("/home/user/highest_centrality.txt", "r") as f:
        content = f.read().strip()
    assert content == "Alice", f"Expected the highest centrality employee to be 'Alice', but got '{content}'."