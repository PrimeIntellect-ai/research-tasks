# test_final_state.py

import os
import json
import sqlite3
import pytest

def get_expected_results(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    query = """
    WITH RECURSIVE SuperAdminRoles AS (
        SELECT role_id
        FROM roles
        WHERE role_name = 'SuperAdmin'

        UNION ALL

        SELECT rh.role_id
        FROM role_hierarchy rh
        INNER JOIN SuperAdminRoles sar ON rh.inherits_role_id = sar.role_id
    )
    SELECT e.id AS emp_id, e.name
    FROM employees e
    INNER JOIN employee_roles er ON e.id = er.emp_id
    INNER JOIN SuperAdminRoles sar ON er.role_id = sar.role_id
    ORDER BY e.id ASC;
    """

    c.execute(query)
    results = [dict(row) for row in c.fetchall()]
    conn.close()
    return results

def test_json_output_exists_and_correct():
    json_path = '/home/user/admin_audit.json'
    db_path = '/home/user/audit.db'

    assert os.path.isfile(json_path), f"Expected JSON output file {json_path} is missing."

    with open(json_path, 'r') as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    expected_data = get_expected_results(db_path)

    assert isinstance(actual_data, list), f"Expected JSON root to be a list, got {type(actual_data).__name__}."
    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} records, got {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert isinstance(actual, dict), f"Expected item at index {i} to be a dictionary."
        assert "emp_id" in actual, f"Missing 'emp_id' key in item at index {i}."
        assert "name" in actual, f"Missing 'name' key in item at index {i}."

        assert actual["emp_id"] == expected["emp_id"], f"Expected emp_id {expected['emp_id']} at index {i}, got {actual['emp_id']}."
        assert actual["name"] == expected["name"], f"Expected name '{expected['name']}' at index {i}, got '{actual['name']}'."

def test_script_uses_cte():
    script_path = '/home/user/audit_report.py'
    assert os.path.isfile(script_path), f"Python script {script_path} is missing."

    with open(script_path, 'r') as f:
        content = f.read().upper()

    assert "WITH RECURSIVE" in content or "WITH " in content, "The script does not seem to use a Common Table Expression (CTE) as required."