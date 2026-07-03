# test_final_state.py

import os
import json
import sqlite3
import pytest

def get_expected_data():
    db_path = '/home/user/audit.db'
    assert os.path.exists(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT emp_id, name, manager_id, dept_id FROM employees")
    employees = cur.fetchall()

    cur.execute("SELECT dept_id, resource FROM permissions")
    permissions = dict(cur.fetchall())

    conn.close()

    emp_dict = {row[0]: row for row in employees}

    def get_path(emp_id):
        path = []
        curr = emp_id
        # To prevent infinite loops in case of bad data
        visited = set()
        while curr is not None and curr not in visited:
            visited.add(curr)
            path.insert(0, str(curr))
            curr = emp_dict[curr][2]
        return "->".join(path)

    expected = []
    for emp_id, name, manager_id, dept_id in employees:
        expected.append({
            "emp_id": emp_id,
            "name": name,
            "resource": permissions.get(dept_id),
            "path": get_path(emp_id)
        })

    expected.sort(key=lambda x: x["emp_id"])
    return expected

def test_compliance_graph_json():
    json_path = '/home/user/compliance_graph.json'
    assert os.path.exists(json_path), f"The output file {json_path} does not exist."
    assert os.path.isfile(json_path), f"{json_path} is not a file."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    assert isinstance(data, list), "The JSON root must be a list of dictionaries."

    expected_data = get_expected_data()

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} records, but found {len(data)}."

    # Check if sorted
    emp_ids = [row.get("emp_id") for row in data]
    assert emp_ids == sorted(emp_ids), "The JSON array is not sorted in ascending order by emp_id."

    for i, (actual_row, expected_row) in enumerate(zip(data, expected_data)):
        assert isinstance(actual_row, dict), f"Item at index {i} is not a dictionary."

        for key in ["emp_id", "name", "resource", "path"]:
            assert key in actual_row, f"Missing key '{key}' in item at index {i}."
            assert actual_row[key] == expected_row[key], (
                f"Mismatch at index {i} for key '{key}': "
                f"expected {expected_row[key]}, got {actual_row[key]}."
            )