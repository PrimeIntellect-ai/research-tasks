# test_final_state.py

import os
import json
import sqlite3
import subprocess
import pytest

DB_PATH = '/home/user/expenses.db'
SCRIPT_PATH = '/home/user/audit.py'
REPORT_PATH = '/home/user/audit_report.json'

def get_expected_data(db_path, dept_name):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    query = """
    WITH CatAvg AS (
        SELECT cat_id, AVG(amount) as raw_avg
        FROM expenses
        GROUP BY cat_id
    )
    SELECT 
        e.name as employee_name,
        d.name as department,
        c.name as category,
        ex.amount as amount,
        ROUND(ca.raw_avg, 2) as category_average,
        ex.date
    FROM expenses ex
    JOIN employees e ON ex.emp_id = e.id
    JOIN departments d ON e.department_id = d.id
    JOIN categories c ON ex.cat_id = c.id
    JOIN CatAvg ca ON ex.cat_id = ca.cat_id
    WHERE d.name = ? AND ex.amount > ca.raw_avg
    ORDER BY ex.date ASC, ex.amount DESC
    """
    c.execute(query, (dept_name,))
    columns = ["employee_name", "department", "category", "amount", "category_average", "date"]
    results = [dict(zip(columns, row)) for row in c.fetchall()]
    conn.close()
    return results

def test_audit_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"The script {SCRIPT_PATH} is missing."

def test_audit_report_json_exists():
    assert os.path.exists(REPORT_PATH), f"The report file {REPORT_PATH} is missing. Did you run the script?"

def test_audit_report_json_contents():
    with open(REPORT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{REPORT_PATH} is not valid JSON.")

    assert isinstance(data, list), f"Expected JSON root to be a list, got {type(data).__name__}."

    expected = get_expected_data(DB_PATH, 'Sales')

    assert len(data) == len(expected), f"Expected {len(expected)} records in report for 'Sales', got {len(data)}."

    for i, (actual_row, expected_row) in enumerate(zip(data, expected)):
        for key in expected_row:
            assert key in actual_row, f"Missing key '{key}' in record {i}."

            if key == 'category_average':
                assert isinstance(actual_row[key], float), f"Expected 'category_average' to be a float, got {type(actual_row[key]).__name__}."
                assert abs(actual_row[key] - expected_row[key]) < 0.001, f"Mismatch in {key} for record {i}: expected {expected_row[key]}, got {actual_row[key]}"
            else:
                assert actual_row[key] == expected_row[key], f"Mismatch in {key} for record {i}: expected {expected_row[key]}, got {actual_row[key]}"

def test_audit_script_dynamic_parameterization():
    # Run the script with 'Engineering' to verify SQL parameterization and dynamic behavior
    result = subprocess.run(['python3', SCRIPT_PATH, 'Engineering'], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed when run with 'Engineering' department. Error: {result.stderr}"

    assert os.path.exists(REPORT_PATH), "Report file was not generated after running script for 'Engineering'."

    with open(REPORT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{REPORT_PATH} is not valid JSON after running for 'Engineering'.")

    expected = get_expected_data(DB_PATH, 'Engineering')
    assert len(data) == len(expected), f"Expected {len(expected)} records for 'Engineering', got {len(data)}. Ensure the department name is correctly parameterized."

    for i, (actual_row, expected_row) in enumerate(zip(data, expected)):
        for key in expected_row:
            assert key in actual_row, f"Missing key '{key}' in record {i} for Engineering."
            if key == 'category_average':
                assert abs(actual_row[key] - expected_row[key]) < 0.001
            else:
                assert actual_row[key] == expected_row[key]