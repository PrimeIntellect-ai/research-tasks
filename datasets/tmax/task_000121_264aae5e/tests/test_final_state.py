# test_final_state.py

import os
import json
import sqlite3
import pytest

def get_expected_roles(db_path, username):
    """Derive the expected roles for a given user directly from the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    WITH RECURSIVE user_role_hierarchy AS (
        -- Base case: direct roles assigned to the user
        SELECT r.id, r.role_name
        FROM users u
        JOIN user_roles ur ON u.id = ur.user_id
        JOIN roles r ON ur.role_id = r.id
        WHERE u.username = ?

        UNION

        -- Recursive step: inherited roles
        SELECT r.id, r.role_name
        FROM user_role_hierarchy urh
        JOIN role_inheritance ri ON urh.id = ri.role_id
        JOIN roles r ON ri.inherits_role_id = r.id
    )
    SELECT DISTINCT role_name FROM user_role_hierarchy ORDER BY role_name;
    """

    cursor.execute(query, (username,))
    roles = [row[0] for row in cursor.fetchall()]
    conn.close()
    return roles

def test_executable_exists():
    """Test that the compiled executable exists."""
    exe_path = "/home/user/audit_tool"
    assert os.path.isfile(exe_path), f"Executable {exe_path} is missing. Did you compile the C program?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_compliance_report_content():
    """Test that the compliance report contains the correct JSON data."""
    report_path = "/home/user/compliance_report.json"
    db_path = "/home/user/audit.db"

    assert os.path.isfile(report_path), f"Report file {report_path} is missing. Did you run the tool?"

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {report_path} does not contain valid JSON.")

    assert isinstance(data, list), "The JSON output must be a list of strings."

    expected_roles = get_expected_roles(db_path, "charlie")

    assert data == expected_roles, (
        f"The roles in {report_path} do not match the expected hierarchy for 'charlie'.\n"
        f"Expected: {expected_roles}\n"
        f"Found: {data}"
    )