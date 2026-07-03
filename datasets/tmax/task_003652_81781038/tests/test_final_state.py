# test_final_state.py

import os
import sqlite3
import json
import pytest

def test_index_exists():
    db_path = "/home/user/company.db"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='index' AND tbl_name='employees';")
    indices = cursor.fetchall()
    conn.close()

    found = False
    for (sql,) in indices:
        if sql and "manager_id" in sql.lower():
            found = True
            break

    assert found, "No index found on the 'manager_id' column in the 'employees' table."

def test_c_source_exists():
    c_file = "/home/user/hierarchy.c"
    assert os.path.isfile(c_file), f"{c_file} not found."

def test_output_json_validity_and_content():
    output_path = "/home/user/output.json"
    assert os.path.isfile(output_path), f"{output_path} not found."

    with open(output_path, "r") as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {output_path} does not contain valid JSON.")

    expected_data = [
        {"id": 3, "name": "Charlie", "depth": 1},
        {"id": 4, "name": "David", "depth": 2},
        {"id": 5, "name": "Eve", "depth": 2},
        {"id": 6, "name": "Frank", "depth": 2}
    ]

    assert actual_data == expected_data, (
        f"JSON output does not match the expected structure and content.\n"
        f"Expected: {expected_data}\n"
        f"Actual: {actual_data}"
    )