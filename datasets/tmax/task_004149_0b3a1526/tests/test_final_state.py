# test_final_state.py

import os
import sqlite3
import json
import pytest

def get_expected_tree(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, manager_id, role FROM employees")
    rows = cursor.fetchall()
    conn.close()

    employees = {}
    for row in rows:
        emp = dict(row)
        emp['subordinates'] = []
        employees[emp['id']] = emp

    root = None
    for emp in employees.values():
        manager_id = emp.pop('manager_id')
        if manager_id is None:
            root = emp
        else:
            employees[manager_id]['subordinates'].append(emp)

    return root

def sort_tree(node):
    if 'subordinates' in node and isinstance(node['subordinates'], list):
        node['subordinates'].sort(key=lambda x: x.get('id', 0))
        for sub in node['subordinates']:
            sort_tree(sub)
    return node

def test_hierarchy_json_correct():
    json_path = "/home/user/hierarchy.json"
    db_path = "/home/user/company.db"

    assert os.path.isfile(json_path), f"Output file {json_path} does not exist. The Go program must write to this file."
    assert os.path.isfile(db_path), f"Database {db_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            actual_tree = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    expected_tree = get_expected_tree(db_path)

    assert expected_tree is not None, "Failed to compute expected tree (no root employee with manager_id IS NULL found)."

    # Sort subordinates by id for stable comparison
    actual_sorted = sort_tree(actual_tree)
    expected_sorted = sort_tree(expected_tree)

    assert actual_sorted == expected_sorted, "The generated JSON does not match the expected hierarchy derived from the 'employees' table."