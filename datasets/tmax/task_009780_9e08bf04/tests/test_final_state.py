# test_final_state.py
import os
import json
import sqlite3

DB_PATH = "/home/user/org.db"
JSON_PATH = "/home/user/dept_summary.json"

def test_db_exists():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."
    assert os.path.isfile(DB_PATH), f"{DB_PATH} is not a file."

def test_db_schema_and_data():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]

    assert "departments" in tables, "Table 'departments' is missing in org.db."
    assert "employees" in tables, "Table 'employees' is missing in org.db."

    # Check schema for departments
    cursor.execute("PRAGMA table_info(departments);")
    dept_cols = {row[1]: row[2].upper() for row in cursor.fetchall()}
    assert "dept_name" in dept_cols, "Column 'dept_name' missing in 'departments' table."
    assert "parent_name" in dept_cols, "Column 'parent_name' missing in 'departments' table."

    # Check schema for employees
    cursor.execute("PRAGMA table_info(employees);")
    emp_cols = {row[1]: row[2].upper() for row in cursor.fetchall()}
    assert "emp_name" in emp_cols, "Column 'emp_name' missing in 'employees' table."
    assert "dept_name" in emp_cols, "Column 'dept_name' missing in 'employees' table."

    # Basic data check
    cursor.execute("SELECT COUNT(*) FROM departments;")
    dept_count = cursor.fetchone()[0]
    assert dept_count >= 5, "Not enough departments extracted into the database."

    cursor.execute("SELECT COUNT(*) FROM employees;")
    emp_count = cursor.fetchone()[0]
    assert emp_count >= 5, "Not enough employees extracted into the database."

    conn.close()

def test_json_summary():
    assert os.path.exists(JSON_PATH), f"Summary JSON file {JSON_PATH} is missing."

    with open(JSON_PATH, "r") as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{JSON_PATH} is not a valid JSON file."

    assert isinstance(summary, dict), "JSON summary should be a dictionary."

    # For the provided truth data, Engineering should have 3 and Sales should have 2
    assert "Engineering" in summary, "Missing 'Engineering' top-level department in JSON."
    assert "Sales" in summary, "Missing 'Sales' top-level department in JSON."

    assert summary["Engineering"] == 3, f"Expected 3 employees under Engineering, got {summary['Engineering']}"
    assert summary["Sales"] == 2, f"Expected 2 employees under Sales, got {summary['Sales']}"