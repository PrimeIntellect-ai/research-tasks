# test_final_state.py

import os
import sqlite3
import pytest

def test_report_content():
    report_path = '/home/user/report.txt'
    assert os.path.exists(report_path), f"Report file {report_path} does not exist."
    assert os.path.isfile(report_path), f"{report_path} is not a file."

    with open(report_path, 'r') as f:
        content = f.read().strip().splitlines()

    expected_lines = [
        "Total Backup Size: 800",
        "Shortest Restore Time: 40"
    ]

    assert len(content) >= 2, f"Report file {report_path} does not contain enough lines."
    assert content[0].strip() == expected_lines[0], f"First line of report is incorrect. Expected '{expected_lines[0]}', got '{content[0].strip()}'"
    assert content[1].strip() == expected_lines[1], f"Second line of report is incorrect. Expected '{expected_lines[1]}', got '{content[1].strip()}'"

def test_backups_table_index():
    db_path = '/home/user/backups.db'
    assert os.path.exists(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Query sqlite_master to find indexes on the backups table
    c.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='backups' AND name NOT LIKE 'sqlite_autoindex%';")
    indexes = c.fetchall()

    conn.close()

    assert len(indexes) > 0, "No custom index found on the 'backups' table. You must create an appropriate index to optimize the query."