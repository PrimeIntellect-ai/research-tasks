# test_final_state.py

import os
import json
import sqlite3
import pytest

DB_PATH = "/home/user/data/company.db"
OUTPUT_PATH = "/home/user/output/dept_costs.json"

def get_expected_results(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    WITH RECURSIVE subordinates AS (
        SELECT subordinate_id 
        FROM reporting_lines 
        JOIN employees ON employees.id = reporting_lines.manager_id
        WHERE employees.name = 'Alice'

        UNION ALL

        SELECT rl.subordinate_id
        FROM reporting_lines rl
        INNER JOIN subordinates s ON s.subordinate_id = rl.manager_id
    )
    SELECT d.name, SUM(e.salary)
    FROM subordinates s
    JOIN employees e ON s.subordinate_id = e.id
    JOIN departments d ON e.department_id = d.id
    GROUP BY d.name
    ORDER BY d.name ASC;
    """

    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    expected_data = []
    for dept, total_salary in results:
        expected_data.append({
            "department": dept,
            "total_salary": float(total_salary)
        })

    return expected_data

def test_output_file_exists():
    assert os.path.exists(OUTPUT_PATH), f"Output file is missing at {OUTPUT_PATH}"
    assert os.path.isfile(OUTPUT_PATH), f"Expected a file at {OUTPUT_PATH}, but found a directory or other type"

def test_output_json_format_and_correctness():
    assert os.path.exists(OUTPUT_PATH), f"Cannot test correctness: {OUTPUT_PATH} is missing"

    with open(OUTPUT_PATH, 'r') as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Output file {OUTPUT_PATH} does not contain valid JSON. Error: {e}")

    assert isinstance(actual_data, list), "The JSON output must be an array of objects"

    expected_data = get_expected_results(DB_PATH)

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} departments in the output, but found {len(actual_data)}"

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert isinstance(actual, dict), f"Item at index {i} is not a JSON object"
        assert "department" in actual, f"Item at index {i} is missing the 'department' key"
        assert "total_salary" in actual, f"Item at index {i} is missing the 'total_salary' key"

        assert actual["department"] == expected["department"], f"Expected department '{expected['department']}' at index {i}, got '{actual['department']}'"

        # Check if it's rounded to 2 decimal places in the raw JSON text (optional but requested by prompt)
        # We'll just verify the numeric value is close enough
        assert isinstance(actual["total_salary"], (int, float)), f"Total salary for {actual['department']} must be a number"
        assert round(actual["total_salary"], 2) == round(expected["total_salary"], 2), f"Incorrect total salary for department {actual['department']}. Expected {expected['total_salary']}, got {actual['total_salary']}"

def test_c_source_code_exists():
    assert os.path.exists("/home/user/etl_graph.c"), "C source code file /home/user/etl_graph.c is missing"