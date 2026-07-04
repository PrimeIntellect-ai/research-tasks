# test_final_state.py
import os
import sqlite3
import pytest

def test_audit_query_script_exists():
    script_path = "/home/user/audit_query.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

def test_database_index_created():
    db_path = "/home/user/access_graph.db"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if any index exists on the 'relations' table
    cursor.execute("PRAGMA index_list('relations')")
    indexes = cursor.fetchall()

    conn.close()

    assert len(indexes) > 0, "No index was created on the 'relations' table."

def test_report_content():
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    expected_lines = [
        "Analytics",
        "App-Server",
        "CI-Server",
        "Cache",
        "Queue"
    ]

    with open(report_path, "r") as f:
        content = f.read().strip().splitlines()

    # Strip whitespace from each line just in case
    content = [line.strip() for line in content if line.strip()]

    assert content == expected_lines, f"Report content is incorrect. Expected {expected_lines}, but got {content}."