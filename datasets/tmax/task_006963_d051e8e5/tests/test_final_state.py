# test_final_state.py

import os
import sqlite3
import csv
import pytest

def test_final_report_exists():
    assert os.path.isfile("/home/user/etl/final_report.csv"), "The file /home/user/etl/final_report.csv is missing."

def test_staging_table_fixed():
    db_path = "/home/user/data/company.db"
    assert os.path.isfile(db_path), f"The database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='stg_emp_dept';")
    assert cursor.fetchone() is not None, "The 'stg_emp_dept' table is missing from the database."

    cursor.execute("SELECT COUNT(*) FROM stg_emp_dept;")
    count = cursor.fetchone()[0]
    conn.close()

    assert count == 6, f"The 'stg_emp_dept' table should have 6 rows, but found {count}. The cartesian product bug might not be fixed."

def test_final_report_content():
    report_path = "/home/user/etl/final_report.csv"

    expected_header = ["emp_id", "emp_name", "dept_name", "management_level", "salary", "dept_running_total"]
    expected_rows = [
        ["1", "Alice", "Engineering", "1", "150000", "150000"],
        ["2", "Bob", "Engineering", "2", "120000", "270000"],
        ["3", "Charlie", "Engineering", "2", "110000", "380000"],
        ["6", "Fiona", "Engineering", "3", "95000", "475000"],
        ["4", "Diana", "Sales", "1", "130000", "130000"],
        ["5", "Evan", "Sales", "2", "90000", "220000"]
    ]

    with open(report_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "The file final_report.csv is empty."

    header = rows[0]
    assert header == expected_header, f"Expected header {expected_header}, but got {header}."

    data_rows = rows[1:]
    assert len(data_rows) == len(expected_rows), f"Expected {len(expected_rows)} data rows, but got {len(data_rows)}."

    for i, (actual, expected) in enumerate(zip(data_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch: expected {expected}, got {actual}."