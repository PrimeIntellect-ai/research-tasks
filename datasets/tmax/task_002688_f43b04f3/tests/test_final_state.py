# test_final_state.py

import os
import json
import sqlite3
import pytest

def test_results_json():
    results_path = "/home/user/app/results.json"
    assert os.path.exists(results_path), f"File {results_path} does not exist."

    with open(results_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} does not contain valid JSON.")

    expected = [
        {"employee_name": "Alice", "project_name": ""},
        {"employee_name": "Bob", "project_name": "Project Alpha"},
        {"employee_name": "Charlie", "project_name": "Project Beta"},
        {"employee_name": "Charlie", "project_name": "Project Gamma"},
        {"employee_name": "Dave", "project_name": ""}
    ]

    # Sort both to ensure order independence
    data_sorted = sorted(data, key=lambda x: (x.get('employee_name', ''), x.get('project_name', '')))
    expected_sorted = sorted(expected, key=lambda x: (x['employee_name'], x['project_name']))

    assert data_sorted == expected_sorted, f"JSON output mismatch.\nExpected: {expected_sorted}\nGot: {data_sorted}"

def test_database_indexes():
    db_path = "/home/user/app/company.db"
    assert os.path.exists(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='employees';")
    emp_indexes = cursor.fetchall()
    assert len(emp_indexes) > 0, "No index found on the 'employees' table."

    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='projects';")
    proj_indexes = cursor.fetchall()
    assert len(proj_indexes) > 0, "No index found on the 'projects' table."

    conn.close()

def test_plan_txt():
    plan_path = "/home/user/app/plan.txt"
    assert os.path.exists(plan_path), f"File {plan_path} does not exist."

    with open(plan_path, "r") as f:
        content = f.read().lower()

    assert "search" in content or "scan" in content, f"File {plan_path} does not appear to contain a valid EXPLAIN QUERY PLAN output (missing SEARCH or SCAN)."

def test_go_module_initialized():
    go_mod_path = "/home/user/app/go.mod"
    go_sum_path = "/home/user/app/go.sum"

    assert os.path.exists(go_mod_path), f"Go module not initialized, {go_mod_path} is missing."
    assert os.path.exists(go_sum_path), f"Go dependencies not installed, {go_sum_path} is missing."

    with open(go_mod_path, "r") as f:
        content = f.read()
        assert "github.com/mattn/go-sqlite3" in content, "go-sqlite3 is not listed in go.mod."