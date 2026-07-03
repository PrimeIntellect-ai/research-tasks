# test_final_state.py

import os
import sqlite3
import csv
import pytest

DB_PATH = "/home/user/corporate.db"
CSV_PATH = "/home/user/audit_report.csv"
CPP_PATH = "/home/user/process_audit.cpp"
BIN_PATH = "/home/user/process_audit"

def test_cpp_files_exist():
    assert os.path.isfile(CPP_PATH), f"C++ source file {CPP_PATH} is missing."
    assert os.path.isfile(BIN_PATH), f"Compiled binary {BIN_PATH} is missing."
    assert os.access(BIN_PATH, os.X_OK), f"Binary {BIN_PATH} is not executable."

def test_index_created():
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} is missing."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_emp_status';")
    idx = cursor.fetchone()
    assert idx is not None, "Index 'idx_emp_status' was not created."

    # Check that the index covers emp_id and status
    cursor.execute("PRAGMA index_info('idx_emp_status');")
    columns = [row[2] for row in cursor.fetchall()]
    assert "emp_id" in columns and "status" in columns, "Index 'idx_emp_status' does not cover 'emp_id' and 'status'."

    conn.close()

def test_csv_report():
    assert os.path.isfile(CSV_PATH), f"CSV report {CSV_PATH} is missing."

    # Compute expected results dynamically
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
    WITH RECURSIVE org_chart AS (
        SELECT id as emp_id, name, department, 0 as depth
        FROM employees
        WHERE id = 1
        UNION ALL
        SELECT e.id, e.name, e.department, o.depth + 1
        FROM employees e
        JOIN org_chart o ON e.manager_id = o.emp_id
    ),
    denied_counts AS (
        SELECT emp_id, COUNT(*) as denied_count
        FROM access_logs
        WHERE status = 'DENIED'
        GROUP BY emp_id
    ),
    combined AS (
        SELECT o.emp_id, o.name, o.department, o.depth, COALESCE(d.denied_count, 0) as denied_count
        FROM org_chart o
        LEFT JOIN denied_counts d ON o.emp_id = d.emp_id
    )
    SELECT emp_id, name, department, depth, denied_count,
           RANK() OVER (PARTITION BY department ORDER BY denied_count DESC, emp_id ASC) as dept_rank
    FROM combined
    """

    cursor.execute(query)
    expected_rows = cursor.fetchall()
    conn.close()

    expected_dicts = []
    for row in expected_rows:
        expected_dicts.append({
            "emp_id": str(row[0]),
            "name": str(row[1]),
            "department": str(row[2]),
            "depth": str(row[3]),
            "denied_count": str(row[4]),
            "dept_rank": str(row[5])
        })

    # Read the actual CSV
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        actual_dicts = list(reader)

    # Check header
    expected_header = ["emp_id", "name", "department", "depth", "denied_count", "dept_rank"]
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        actual_header = f.readline().strip().split(",")
    assert actual_header == expected_header, f"CSV header is incorrect. Expected {expected_header}, got {actual_header}."

    # Sort both lists of dicts to compare
    def sort_key(d):
        return (int(d["emp_id"]))

    expected_dicts.sort(key=sort_key)
    actual_dicts.sort(key=sort_key)

    assert len(actual_dicts) == len(expected_dicts), f"Expected {len(expected_dicts)} rows in CSV, found {len(actual_dicts)}."

    for actual, expected in zip(actual_dicts, expected_dicts):
        assert actual == expected, f"Row mismatch. Expected {expected}, got {actual}."