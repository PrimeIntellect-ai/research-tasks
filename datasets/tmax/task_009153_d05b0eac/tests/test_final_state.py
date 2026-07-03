# test_final_state.py

import os
import json
import sqlite3
import pytest

REPORT_PATH = '/home/user/compliance_report.json'
DB_PATH = '/home/user/audit.db'

def get_expected_data():
    """Derives the expected report data directly from the current state of the database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
    WITH RECURSIVE hierarchy AS (
        SELECT emp_id, 0 AS hierarchy_level 
        FROM employees 
        WHERE manager_id IS NULL

        UNION ALL

        SELECT e.emp_id, h.hierarchy_level + 1
        FROM employees e
        JOIN hierarchy h ON e.manager_id = h.emp_id
    ),
    system_counts AS (
        SELECT emp_id, system_name, COUNT(*) as access_count
        FROM access_logs
        GROUP BY emp_id, system_name
    ),
    ranked_systems AS (
        SELECT emp_id, system_name, access_count,
               ROW_NUMBER() OVER (PARTITION BY emp_id ORDER BY access_count DESC, system_name ASC) as rn
        FROM system_counts
    )
    SELECT h.emp_id as employee_id, 
           h.hierarchy_level, 
           r.system_name as top_system, 
           r.access_count as top_system_access_count
    FROM hierarchy h
    JOIN ranked_systems r ON h.emp_id = r.emp_id AND r.rn = 1
    ORDER BY h.emp_id ASC;
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

def test_report_exists():
    """Test that the compliance report JSON file was created."""
    assert os.path.exists(REPORT_PATH), f"Report file {REPORT_PATH} is missing."
    assert os.path.isfile(REPORT_PATH), f"{REPORT_PATH} should be a file."

def test_report_format_and_content():
    """Test that the compliance report contains the correct JSON structure and data."""
    assert os.path.exists(REPORT_PATH), f"Report file {REPORT_PATH} is missing."

    with open(REPORT_PATH, 'r') as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {REPORT_PATH} does not contain valid JSON.")

    assert isinstance(report_data, list), "The JSON root must be an array (list)."

    expected_data = get_expected_data()

    assert len(report_data) == len(expected_data), (
        f"Expected {len(expected_data)} records in the report, but found {len(report_data)}. "
        "Ensure employees with no access logs are excluded."
    )

    for i, (actual, expected) in enumerate(zip(report_data, expected_data)):
        assert isinstance(actual, dict), f"Item at index {i} is not a JSON object."

        assert actual.get("employee_id") == expected["employee_id"], \
            f"Record {i}: Expected employee_id {expected['employee_id']}, got {actual.get('employee_id')}."

        assert actual.get("hierarchy_level") == expected["hierarchy_level"], \
            f"Record {i} (employee {expected['employee_id']}): Expected hierarchy_level {expected['hierarchy_level']}, got {actual.get('hierarchy_level')}."

        assert actual.get("top_system") == expected["top_system"], \
            f"Record {i} (employee {expected['employee_id']}): Expected top_system '{expected['top_system']}', got '{actual.get('top_system')}'. Check tie-breaking logic."

        assert actual.get("top_system_access_count") == expected["top_system_access_count"], \
            f"Record {i} (employee {expected['employee_id']}): Expected top_system_access_count {expected['top_system_access_count']}, got {actual.get('top_system_access_count')}."