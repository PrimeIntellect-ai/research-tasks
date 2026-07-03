# test_final_state.py

import os
import sqlite3
import json
import csv
import pytest

DB_PATH = '/home/user/company.db'
JSON_PATH = '/home/user/graph_data.json'
CSV_PATH = '/home/user/cross_dept_collabs.csv'

def test_indexes_created():
    """Check if indexes were added to the database to optimize queries."""
    assert os.path.exists(DB_PATH), f"Database file not found at {DB_PATH}"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_autoindex%'")
    indexes = cursor.fetchall()
    conn.close()

    assert len(indexes) > 0, "No custom indexes found in the database. You need to add indexes to optimize query performance."
    # Check if there's an index on employee_projects at least
    indexed_tables = {row[1] for row in indexes}
    assert 'employee_projects' in indexed_tables or 'employees' in indexed_tables, "Expected indexes on employee_projects or employees tables."

def test_json_output_format():
    """Check if graph_data.json exists and has the correct format."""
    assert os.path.exists(JSON_PATH), f"JSON file not found at {JSON_PATH}"

    with open(JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("graph_data.json is not a valid JSON file.")

    assert isinstance(data, list), "JSON root must be a list."

    if len(data) > 0:
        first_item = data[0]
        assert "employee_id" in first_item, "Missing 'employee_id' in JSON objects."
        assert "department_id" in first_item, "Missing 'department_id' in JSON objects."
        assert "projects" in first_item, "Missing 'projects' in JSON objects."
        assert isinstance(first_item["projects"], list), "'projects' must be a list."

def test_csv_output_correctness():
    """Check if cross_dept_collabs.csv exists and contains the exact correct pairs."""
    assert os.path.exists(CSV_PATH), f"CSV file not found at {CSV_PATH}"

    # Compute the expected result from the database directly
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
    SELECT e1.id AS emp1_id, e2.id AS emp2_id, ep1.proj_id AS shared_project_id
    FROM employees e1
    JOIN employee_projects ep1 ON e1.id = ep1.emp_id
    JOIN employee_projects ep2 ON ep1.proj_id = ep2.proj_id
    JOIN employees e2 ON ep2.emp_id = e2.id
    WHERE e1.id < e2.id AND e1.dept_id != e2.dept_id
    ORDER BY e1.id ASC, e2.id ASC, ep1.proj_id ASC
    """

    cursor.execute(query)
    expected_rows = cursor.fetchall()
    conn.close()

    expected_data = [(str(row[0]), str(row[1]), str(row[2])) for row in expected_rows]

    actual_data = []
    with open(CSV_PATH, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        assert headers == ['emp1_id', 'emp2_id', 'shared_project_id'], "CSV headers are incorrect."

        for row in reader:
            if len(row) == 3:
                actual_data.append(tuple(row))

    assert actual_data == expected_data, "The data in cross_dept_collabs.csv does not match the expected output based on the database."