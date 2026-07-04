# test_final_state.py
import os
import stat
import json
import sqlite3
import pytest

def test_audit_pipeline_script_exists_and_executable():
    script_path = '/home/user/audit_pipeline.sh'
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"The script {script_path} is not executable by the user."

def test_violations_json_exists():
    json_path = '/home/user/violations.json'
    assert os.path.exists(json_path), f"The output file {json_path} does not exist."
    assert os.path.isfile(json_path), f"{json_path} is not a file."

def test_violations_json_content():
    json_path = '/home/user/violations.json'
    db_path = '/home/user/sys_audit.db'

    # Read the JSON file
    try:
        with open(json_path, 'r') as f:
            actual_data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {json_path} does not contain valid JSON.")

    assert isinstance(actual_data, list), f"The JSON in {json_path} must be an array."

    # Derive the expected violations from the database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    query = """
    SELECT 
        u.name AS user, 
        r.name AS resource, 
        d.name AS resource_department
    FROM edges e_acc
    JOIN nodes u ON e_acc.source = u.id AND u.type = 'User'
    JOIN nodes r ON e_acc.target = r.id AND r.type = 'Resource'
    JOIN edges e_bel ON e_bel.source = r.id AND e_bel.relation = 'BELONGS_TO'
    JOIN nodes d ON e_bel.target = d.id AND d.type = 'Department'
    WHERE e_acc.relation = 'ACCESSED'
      AND NOT EXISTS (
          SELECT 1 FROM edges e_mem
          WHERE e_mem.source = u.id 
            AND e_mem.target = d.id 
            AND e_mem.relation = 'MEMBER_OF'
      )
    ORDER BY u.name ASC, r.name ASC
    """

    c.execute(query)
    expected_rows = c.fetchall()
    conn.close()

    expected_data = [
        {"user": row[0], "resource": row[1], "resource_department": row[2]}
        for row in expected_rows
    ]

    # Check length
    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} violations, found {len(actual_data)}."

    # Check each item in order
    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert isinstance(actual, dict), f"Item at index {i} is not a JSON object."

        # Check keys
        expected_keys = {"user", "resource", "resource_department"}
        actual_keys = set(actual.keys())
        assert actual_keys == expected_keys, f"Item at index {i} has incorrect keys. Expected {expected_keys}, found {actual_keys}."

        # Check values
        assert actual["user"] == expected["user"], f"Item at index {i} has wrong user. Expected '{expected['user']}', found '{actual['user']}'."
        assert actual["resource"] == expected["resource"], f"Item at index {i} has wrong resource. Expected '{expected['resource']}', found '{actual['resource']}'."
        assert actual["resource_department"] == expected["resource_department"], f"Item at index {i} has wrong resource_department. Expected '{expected['resource_department']}', found '{actual['resource_department']}'."