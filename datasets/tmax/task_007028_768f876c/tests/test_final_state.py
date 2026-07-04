# test_final_state.py

import os
import sqlite3
import json

def test_sqlite_database_and_schema():
    db_path = "/home/user/org.db"
    assert os.path.exists(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check table existence
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='employees';")
    assert cursor.fetchone() is not None, "Table 'employees' does not exist in the database."

    # Check schema
    cursor.execute("PRAGMA table_info(employees);")
    columns = {row[1]: row[2] for row in cursor.fetchall()}

    assert "emp_id" in columns, "Column 'emp_id' missing."
    assert "name" in columns, "Column 'name' missing."
    assert "manager_id" in columns, "Column 'manager_id' missing."
    assert "salary" in columns, "Column 'salary' missing."

    # Check data is loaded
    cursor.execute("SELECT COUNT(*) FROM employees;")
    count = cursor.fetchone()[0]
    assert count > 0, "The 'employees' table is empty."
    conn.close()

def test_hierarchy_budgets_csv():
    jsonl_path = "/home/user/raw_org.jsonl"
    csv_path = "/home/user/hierarchy_budgets.csv"

    assert os.path.exists(csv_path), f"CSV file {csv_path} does not exist."

    # Recompute expected budgets
    employees = {}
    with open(jsonl_path, 'r') as f:
        for line in f:
            if line.strip():
                data = json.loads(line)
                employees[data["emp_id"]] = {
                    "salary": data["salary"],
                    "manager_id": data["manager_id"]
                }

    # Build tree
    children = {emp_id: [] for emp_id in employees}
    for emp_id, data in employees.items():
        mgr = data["manager_id"]
        if mgr and mgr in children:
            children[mgr].append(emp_id)

    def get_budget(emp_id):
        total = employees[emp_id]["salary"]
        for child in children[emp_id]:
            total += get_budget(child)
        return total

    budgets = []
    for emp_id in employees:
        budgets.append((emp_id, get_budget(emp_id)))

    # Sort by total_budget DESC, then emp_id ASC
    budgets.sort(key=lambda x: (-x[1], x[0]))

    expected_lines = [f"{emp_id},{budget}" for emp_id, budget in budgets]

    with open(csv_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} rows in CSV, got {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Row {i+1} mismatch. Expected '{expected}', got '{actual}'."

def test_recursive_sql():
    sql_path = "/home/user/recursive.sql"
    assert os.path.exists(sql_path), f"SQL file {sql_path} does not exist."

    with open(sql_path, 'r') as f:
        content = f.read().upper()

    assert "WITH RECURSIVE" in content, f"The query in {sql_path} does not seem to use a Recursive CTE (missing 'WITH RECURSIVE')."

def test_explain_plan():
    plan_path = "/home/user/plan.txt"
    assert os.path.exists(plan_path), f"Plan file {plan_path} does not exist."

    with open(plan_path, 'r') as f:
        content = f.read().strip()

    assert len(content) > 0, f"The file {plan_path} is empty."
    # Basic check for EXPLAIN output characteristics
    assert "SCAN" in content.upper() or "SEARCH" in content.upper() or "EXECUTE" in content.upper(), \
        f"The file {plan_path} does not look like valid SQLite EXPLAIN QUERY PLAN output."