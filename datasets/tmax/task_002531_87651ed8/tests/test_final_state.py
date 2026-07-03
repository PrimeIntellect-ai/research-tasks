# test_final_state.py

import os
import json
import sqlite3
import pytest

REPORT_PATH = '/home/user/compliance_report.json'
DB_PATH = '/home/user/audit_data.db'

def test_compliance_report_exists():
    """Test that the compliance report JSON file was created."""
    assert os.path.exists(REPORT_PATH), f"Report file not found at {REPORT_PATH}"
    assert os.path.isfile(REPORT_PATH), f"{REPORT_PATH} is not a file"

def test_compliance_report_content():
    """Test that the compliance report contains the correct aggregated violations."""
    assert os.path.exists(REPORT_PATH), f"Missing {REPORT_PATH}"

    with open(REPORT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{REPORT_PATH} does not contain valid JSON")

    expected_data = [
        {
            "emp_id": 1,
            "name": "Alice",
            "violation_count": 3
        },
        {
            "emp_id": 3,
            "name": "Charlie",
            "violation_count": 2
        }
    ]

    assert isinstance(data, list), "The JSON output must be an array of objects"
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} records, got {len(data)}"

    for i, expected in enumerate(expected_data):
        assert data[i] == expected, f"Record at index {i} does not match expected output. Expected {expected}, got {data[i]}"

def test_indexes_created():
    """Test that indexes were created on the database to optimize queries."""
    assert os.path.exists(DB_PATH), f"Database file missing at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_autoindex%';")
    indexes = cursor.fetchall()
    conn.close()

    assert len(indexes) > 0, "No indexes were created on the database. The task requires creating indexes to optimize queries."