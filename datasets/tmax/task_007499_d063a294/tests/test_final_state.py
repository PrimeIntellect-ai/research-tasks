# test_final_state.py

import os
import sys
import json
import sqlite3
import subprocess
import pytest

def get_expected_data(db_path):
    query = """
    WITH RECURSIVE
      hierarchy AS (
        SELECT id, name, manager_id, department, salary, 0 AS hierarchy_level
        FROM employees
        WHERE manager_id IS NULL
        UNION ALL
        SELECT e.id, e.name, e.manager_id, e.department, e.salary, h.hierarchy_level + 1
        FROM employees e
        JOIN hierarchy h ON e.manager_id = h.id
      )
    SELECT
      id,
      name,
      department,
      salary,
      hierarchy_level,
      SUM(salary) OVER(PARTITION BY department) AS dept_total_salary,
      RANK() OVER(PARTITION BY department ORDER BY salary DESC) AS dept_salary_rank
    FROM hierarchy;
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    expected = []
    for row in rows:
        expected.append({
            "id": row["id"],
            "name": row["name"],
            "department": row["department"],
            "salary": row["salary"],
            "hierarchy_level": row["hierarchy_level"],
            "dept_total_salary": row["dept_total_salary"],
            "dept_salary_rank": row["dept_salary_rank"]
        })
    return expected

def test_script_execution_and_output():
    script_path = "/home/user/export_metrics.py"
    output_path = "/home/user/metrics_output.json"
    db_path = "/home/user/company.db"

    assert os.path.isfile(script_path), f"Script not found at {script_path}"

    # Run the script
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. stderr: {result.stderr}"

    assert os.path.isfile(output_path), f"Output file not generated at {output_path}"

    with open(output_path, "r") as f:
        try:
            output_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {output_path} is not valid JSON.")

    assert isinstance(output_data, list), "Output JSON must be a list of objects."

    expected_data = get_expected_data(db_path)

    # Sort both lists by id for comparison
    output_data_sorted = sorted(output_data, key=lambda x: x.get("id", -1))
    expected_data_sorted = sorted(expected_data, key=lambda x: x["id"])

    assert len(output_data_sorted) == len(expected_data_sorted), f"Expected {len(expected_data_sorted)} records, got {len(output_data_sorted)}"

    for actual, expected in zip(output_data_sorted, expected_data_sorted):
        assert actual == expected, f"Record mismatch. Expected: {expected}, Got: {actual}"