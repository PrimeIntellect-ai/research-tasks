# test_final_state.py
import os
import sqlite3
import re
import pytest

DB_PATH = "/home/user/compliance.db"
CARGO_TOML_PATH = "/home/user/access_auditor/Cargo.toml"
RESULT_TXT_PATH = "/home/user/audit_result.txt"
OPTIMIZE_SQL_PATH = "/home/user/optimize.sql"

def test_cargo_project_exists():
    """Verify that the Cargo project was created."""
    assert os.path.exists(CARGO_TOML_PATH), f"Cargo project not found. Expected Cargo.toml at {CARGO_TOML_PATH}"

def test_audit_result():
    """Verify that audit_result.txt contains the correct result derived from the database."""
    assert os.path.exists(RESULT_TXT_PATH), f"Audit result file not found at {RESULT_TXT_PATH}"

    # Compute the expected result directly from the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = """
        SELECT e.name, COUNT(r.id) as cnt
        FROM employees e
        JOIN access_grants ag ON e.id = ag.emp_id
        JOIN resources r ON ag.resource_id = r.id
        WHERE e.department = 'Finance' AND r.sensitivity = 'HIGH'
        GROUP BY e.id
        ORDER BY cnt DESC, e.id ASC
        LIMIT 1;
    """
    cursor.execute(query)
    row = cursor.fetchone()
    conn.close()

    assert row is not None, "Could not compute expected result from the database."
    expected_output = f"{row[0]}:{row[1]}"

    with open(RESULT_TXT_PATH, "r") as f:
        actual_content = f.read().strip()

    assert expected_output in actual_content, f"Expected '{expected_output}' in {RESULT_TXT_PATH}, but found '{actual_content}'"

def test_optimize_sql_indexes():
    """Verify that optimize.sql contains the correct CREATE INDEX statements."""
    assert os.path.exists(OPTIMIZE_SQL_PATH), f"SQL optimization file not found at {OPTIMIZE_SQL_PATH}"

    with open(OPTIMIZE_SQL_PATH, "r") as f:
        content = f.read().lower()

    # Check for index on employees(department)
    assert re.search(r"create\s+(?:unique\s+)?index\s+.*?\s+on\s+employees\s*\(\s*.*?department.*?\s*\)", content), \
        "Missing CREATE INDEX statement for employees table on the department column."

    # Check for index on resources(sensitivity)
    assert re.search(r"create\s+(?:unique\s+)?index\s+.*?\s+on\s+resources\s*\(\s*.*?sensitivity.*?\s*\)", content), \
        "Missing CREATE INDEX statement for resources table on the sensitivity column."

    # Check for index on access_grants(emp_id) and/or access_grants(resource_id)
    has_emp_id = re.search(r"create\s+(?:unique\s+)?index\s+.*?\s+on\s+access_grants\s*\(\s*.*?emp_id.*?\s*\)", content)
    has_res_id = re.search(r"create\s+(?:unique\s+)?index\s+.*?\s+on\s+access_grants\s*\(\s*.*?resource_id.*?\s*\)", content)

    assert has_emp_id or has_res_id, \
        "Missing CREATE INDEX statement for access_grants table on emp_id and/or resource_id columns."